from collections import Counter

from tools import Tool


class KeyCounter:
    """
    Counter that analyze the availability of proxies.
    """

    def __init__(self):
        self._before = None
        self._after = None
        self._keys_before = None

    def set_before_number(self, data: list):
        """
        :param data: proxy list before filtering
        :type data: list
        """

        key_list_before = []
        for i in data:
            key, = i.keys()
            key_list_before.append(key)

        result_before = Counter(key_list_before)
        self._before = dict(result_before)
        [*self._keys_before] = self._before.keys()

    def set_after_number(self, data: list):
        """
        :param data: proxies list after filtering
        :type data: list
        """

        key_list_after = []
        for i in data:
            key, = i.keys()
            key_list_after.append(key)

        result_after = Counter(key_list_after)
        self._after = dict(result_after)
        for key_before in self._keys_before:
            if key_before not in key_list_after:
                self._after[f'{key_before}'] = 0

    def report(self):
        """
        Print proxy availability
        """

        for key in self._keys_before:
            per = self._after[key] / self._before[key]
            Tool.info(f'{key}: {per:.2%}')

    def _flush(self):
        self._before = None
        self._after = None
        self._keys_before = None



if __name__ == '__main__':
    a = [{'KuaiDaiLi': {'http': 'http://342.343.23:2009'}},
         {'IP66': {'http': 'http://342.343.23:2009'}},
         {'KuaiDaiLi': {'http': 'http://342.343.23:2009'}}]
    b = [{'KuaiDaiLi': {'http': 'http://342.343.23:2009'}},
         {'KuaiDaiLi': {'http': 'http://342.343.23:2009'}}]

    c = KeyCounter()
    c.set_before_number(a)
    c.set_after_number(b)
