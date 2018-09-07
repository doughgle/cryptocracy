
import unittest
from hypothesis import given
from hypothesis.strategies import text

from src.model.key_spec import keys, assert_valid
from src.model.proxy_key_generator import ProxyKeyGenerator


class TestProxyKeyGen(unittest.TestCase):

    @given(msk=keys(), pkcs=keys(), pku=keys(), attribute_expr=text())
    def test_returns_non_empty_key(self, msk, pkcs, pku, attribute_expr):
        proxykey_user = ProxyKeyGenerator(msk).generate(pku, pkcs, attribute_expr)
        self.assertTrue(proxykey_user)

    @given(msk=keys(), pkcs=keys(), pku=keys(), attribute_expr=text())
    def test_same_inputs_different_key(self, msk, pkcs, pku, attribute_expr):
        proxykey_a = ProxyKeyGenerator(msk).generate(pku, pkcs, attribute_expr)
        proxykey_b = ProxyKeyGenerator(msk).generate(pku, pkcs, attribute_expr)
        self.assertNotEqual(proxykey_a, proxykey_b)

    @given(msk=keys(), pkcs=keys(), pku=keys(), attribute_expr=text())
    def test_key_meets_key_spec(self, msk, pkcs, pku, attribute_expr):
        proxy_key = ProxyKeyGenerator(msk).generate(pku, pkcs, attribute_expr)
        assert_valid(proxy_key)


if __name__ == '__main__':
    unittest.main()
