
import unittest
from hypothesis import given
from hypothesis.strategies import text

from oabe_proxykeygen import proxykeygen

class TestProxyKeyGen(unittest.TestCase):

    @given(msk=text(), pkcs=text(), pku=text(), attribute_expr=text())
    def test_returns_non_empty_key(self, msk, pkcs, pku, attribute_expr):
        proxykey_user = proxykeygen(msk, pkcs, pku, attribute_expr)
        self.assertTrue(proxykey_user)


if __name__ == '__main__':
    unittest.main()
