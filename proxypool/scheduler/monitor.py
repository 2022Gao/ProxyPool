import time
from tools import Tool
from multiprocessing import Process

from proxypool.database import RedisOperator
from proxypool.scheduler import PoolAdder
from proxypool.scheduler import ProxyFilter


class ExpireCheckProcess(Process):
    """
    Specify a cycle, each cycle check part of the proxy.
    """

    def __init__(self, cycle):
        """
        :param cycle: cycle size
        """
        super().__init__()
        self._cycle = cycle

        self._tester = ProxyFilter()
        # self.daemon = True

    def run(self):
        pool = RedisOperator()
        Tool.info('Expire check process is working...')

        while True:
            time.sleep(self._cycle)
            total = int(0.25 * pool.size)
            if total < 4:
                continue
            raw_proxies = [pool.pop() for _ in range(total)]
            self._tester.set_raw_proxies(raw_proxies)
            self._tester.filter()
            proxies = self._tester.usable_proxies
            if len(proxies) != 0:
                pool.puts(proxies)


class ProxyCountCheckProcess(Process):
    """
    Specify a cycle, each cycle check the number of proxies.
    """

    def __init__(self, lower_threshold, upper_threshold, cycle):

        super().__init__()
        self._lower_threshold = lower_threshold
        self._upper_threshold = upper_threshold
        self._cycle = cycle

    def run(self):
        Tool.info('Proxy count check process is working...')
        adder = PoolAdder()
        pool = RedisOperator()
        while True:
            if pool.size < self._lower_threshold:
                Tool.info('Pool size is less than lower threshold, fire PoolAdder.')
                adder.add_to_pool()
            time.sleep(self._cycle)


if __name__ == '__main__':
    a = ExpireCheckProcess(3)
