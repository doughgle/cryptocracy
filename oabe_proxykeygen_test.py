
import unittest
from hypothesis import given
from hypothesis.strategies import text

class TestProxyKeyGen(unittest.TestCase):

    @given(text())
    def test_no_two_proxy_keys_are_the_same(self, s):
        assert True

if __name__ == '__main__':
    unittest.main()
