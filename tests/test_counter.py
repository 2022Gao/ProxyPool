import unittest

from counter import KeyCounter

LIST_BEFORE = [{'k1': 'v1'}, {'k2': 'v2'}, {'k1': 'v1'}]
LIST_AFTER = [{'k1': 'v1'}, {'k1': 'v1'}]


class KeyCounterTestCase(unittest.TestCase):

    def setUp(self):
        self.operator = KeyCounter()

    def tearDown(self) -> None:
        self.operator._flush()

    def test_set_before_number(self):
        self.operator.set_before_number(LIST_BEFORE)

        assert self.operator._keys_before == ['k1', 'k2']

    def test_set_after_number(self):
        self.operator._before = {'k1': 2, 'k2': 1}
        self.operator._keys_before = ['k1', 'k2']
        self.operator.set_after_number(LIST_AFTER)

        assert self.operator._after == {'k1': 2, 'k2': 0}


if __name__ == '__main__':
    unittest.main()
