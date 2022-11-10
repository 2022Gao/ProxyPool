from concurrent import futures

from counter import KeyCounter
from proxypool.conf import POOL_UPPER_THRESHOLD
from proxypool.database import RedisOperator
from proxypool.errors import ResourceDepletionError
from proxypool.scheduler.filter import ProxyFilter
from proxypool.spiders import SpiderMeta
from tools import Tool


class PoolAdder:
    """
    Proxy Adder
    Add filtered proxies to the database.
    """

    def __init__(self):
        """
        Get the redis operator and connect to database.
        Get the tool of filter proxies.
        """
        self._threshold = POOL_UPPER_THRESHOLD
        self._pool = RedisOperator()
        self._tester = ProxyFilter()
        self._counter = KeyCounter()

    def is_over(self):
        """
        Determine if the proxy pool is full.
        :return: True or False
        """
        if self._pool.size >= self._threshold:
            return True
        else:
            return False

    def add_to_pool(self):

        Tool.info('PoolAdder is working...')
        spiders = [cls() for cls in SpiderMeta.spiders]

        flag = 0
        while not self.is_over():

            flag += 1
            Tool.info(f'Start add proxies for the {flag}th time...')
            raw_proxies = []
            with futures.ThreadPoolExecutor(max_workers=len(spiders)) as executor:
                future_to_down = [executor.submit(spiders[i].get, 5) for i in range(len(spiders))]

                for future in futures.as_completed(future_to_down):
                    raw_proxies.extend(future.result())

            self._counter.set_before_number(raw_proxies)

            # Below is the interface of filtering proxies
            self._tester.set_raw_proxies(raw_proxies)
            self._tester.filter()
            proxies = self._tester.usable_proxies

            self._counter.set_after_number(proxies)
            self._counter.report()

            if len(proxies) != 0:
                self._pool.puts(proxies)
            if self.is_over():
                break
            if flag >= 5:
                raise ResourceDepletionError


if __name__ == '__main__':
    pass
