from proxypool.database import RedisOperator
import unittest


class RedisOperatorTestCase(unittest.TestCase):

    def setUp(self):
        self.operator = RedisOperator()

    def tearDown(self):
        self.operator._flush()

    def test_puts_and_pop(self):
        self.operator.puts([dict({'k1': 'v1'})])
        assert self.operator.pop() == dict({'k1': 'v1'})
        proxy_list = [dict({'k1': 'v1'}), dict({'k1': 'v1'}), dict({'k2': 'v2'}), dict({'k3': 'v3'})]
        self.operator.puts(proxy_list)
        init_size = self.operator.size
        self.operator.pop()
        assert self.operator.size == init_size - 1

    def test_size(self):
        proxy_list = [dict({'k1': 'v1'}), dict({'k1': 'v1'}), dict({'k2': 'v2'}), dict({'k3': 'v3'})]
        self.operator.puts(proxy_list)
        assert self.operator.size == 3

    def test_gets(self):
        init_size = self.operator.size
        self.operator.gets(3)
        assert self.operator.size == init_size


if __name__ == '__main__':
    unittest.main()
