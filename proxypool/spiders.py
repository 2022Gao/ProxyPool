import time

import requests

from proxypool.errors import RewriteSpiderError
from proxypool.utils import get_page


class SpiderMeta(type):
    """
    Spider metaclass
    """
    spiders = []

    def _init(cls):
        """
        :return: None
        """
        cls._counter = 1

    def _increment(cls, count):
        """
        :param count: counter increment
        :return: None
        """
        cls._counter += count

    def _flush(cls):
        """
        :return: None
        """
        cls._counter = 1

    def __new__(mcs, *args: tuple, **kwargs: dict):
        """
        :param args: args[0]=new spider name; args[1]=metaclass name; args[2]=new spider's functions
        :param kwargs: None
        :return: a new spider class
        """

        # new spider class must have 'get' function
        if 'get' not in args[2]:
            raise RewriteSpiderError(args[0])

        # set default method to new spider class
        args[2]['__init__'] = lambda self: SpiderMeta._init(self)
        args[2]['increment'] = lambda self, count: SpiderMeta._increment(self, count)
        args[2]['flush'] = lambda self: SpiderMeta._flush(self)

        # put new spider class in 'spiders' list
        SpiderMeta.spiders.append(type.__new__(mcs, *args, **kwargs))
        return type.__new__(mcs, *args, **kwargs)


# Here is the custom crawler class
class KuaiDaiLi(metaclass=SpiderMeta):
    index_url = 'https://www.kuaidaili.com/free/inha/{page}/'

    def get(self, page_increments=3):

        urls = [self.index_url.format(page=p)
                for p in range(self._counter, self._counter + page_increments)]
        self.increment(page_increments)

        proxies = []
        for url in urls:
            html = get_page(url=url)
            time.sleep(1)

            temp = []
            for item in html('table tr').items():
                host = item('td[data-title="IP"]').text()
                port = item('td[data-title="PORT"]').text()
                protocol = item('td[data-title="类型"]').text().lower()
                if host and port and protocol:
                    proxy = {protocol: protocol + '://' + host + ':' + port}
                    metadata = {'KuaiDaiLi': proxy}
                    temp.append(metadata)
            proxies.extend(temp)

        return proxies


class Ip66(metaclass=SpiderMeta):
    index_url = 'http://www.66ip.cn/{page}.html'

    def get(self, page_increments=3):
        urls = [self.index_url.format(page=p)
                for p in range(self._counter, self._counter + page_increments)]
        self.increment(page_increments)

        proxies = []
        for url in urls:
            html = get_page(url=url)
            time.sleep(1)
            trs = html('table tr:gt(0)').items()

            temp = []
            for tr in trs:
                host = tr('td:nth-child(1)').text()
                port = tr('td:nth-child(2)').text()
                protocol = 'http'
                if host and port and protocol:
                    proxy = {protocol: protocol + '://' + host + ':' + port}
                    metadata = {'Ip66': proxy}
                    temp.append(metadata)

            proxies.extend(temp)

        return proxies


class PzzQz(metaclass=SpiderMeta):
    index_url = 'https://pzzqz.com/'

    def get(self, page_increments=None):

        html = get_page(url=self.index_url)
        trs = html('table tr:gt(0)').items()
        proxies = []
        for tr in trs:
            host = tr('td:nth-child(1)').text()
            port = tr('td:nth-child(2)').text()
            protocol = tr('td:nth-child(5)').text().lower()
            if host and port and protocol:
                if protocol in ['socks4', 'socks5']:
                    proxy = {'http': protocol + '://' + host + ':' + port,
                             'https': protocol + '://' + host + ':' + port}
                else:
                    proxy = {protocol: protocol + '://' + host + ':' + port}
                metadata = {'PzzQz': proxy}
                proxies.append(metadata)

        return proxies


class FateZero(metaclass=SpiderMeta):
    index_url = 'http://proxylist.fatezero.org/proxy.list'

    def get(self, page_increments=None):

        try:
            response = requests.get(url=self.index_url, timeout=10)
            text = response.text

        except requests.Timeout:
            pass
        except Exception:
            pass
        else:
            result = text.split('\n')
            proxies = []

            for item in list(result):

                try:
                    dict_item = eval(item)
                except Exception:
                    pass
                else:
                    host = dict_item['host']
                    port = str(dict_item['port'])
                    protocol = dict_item['type']
                    if host and port and protocol:
                        if protocol in ['socks4', 'socks5']:
                            proxy = {'http': protocol + '://' + host + ':' + port,
                                     'https': protocol + '://' + host + ':' + port}
                        else:
                            proxy = {protocol: protocol + '://' + host + ':' + port}
                        metadata = {'FateZero': proxy}
                        proxies.append(metadata)

            return proxies


if __name__ == '__main__':
    pass
