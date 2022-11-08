from concurrent import futures

import requests

from proxypool.conf import TEST_API, HEADERS


class ProxyFilter(object):
    """
    Proxy Filter
    Filter out unavailable proxies.
    """

    def __init__(self):
        self.raw_proxies = None
        self._usable_proxies = None

    def set_raw_proxies(self, raw_proxies: list):
        """
        :param raw_proxies: A list with Proxy as element.
        """

        self.raw_proxies = raw_proxies
        self._usable_proxies = []

    def filter_function(self, metadata: dict):
        """
        :param metadata: single proxy
        :type metadata: dict
        :return: usable proxies
        """
        proxy, = metadata.values()

        try:
            response = requests.get(url=TEST_API,
                                    headers=HEADERS,
                                    timeout=15,
                                    proxies=proxy)
            if response.status_code == 200:
                self._usable_proxies.append(metadata)

        except requests.Timeout as t:
            pass
        except requests.RequestException as r:
            pass
        except Exception as e:
            pass

    def filter(self):
        """
        Test Executor
        """

        max_workers = int(len(self.raw_proxies) / 10)
        if max_workers < 1:
            max_workers = 1

        with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.filter_function, self.raw_proxies)

    @property
    def usable_proxies(self):
        return self._usable_proxies


if __name__ == '__main__':
    pass
