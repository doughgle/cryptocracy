
import unittest

from hypothesis import given

from src.model.cipher import OpenABECipher
from src.model.key_spec import keys, assert_valid
from src.model.policy_expression_spec import attributes
from src.model.proxy_key_generator import ProxyKeyGenerator


class TestProxyKeyGen(unittest.TestCase):

    def setUp(self):
        self.key_gen = ProxyKeyGenerator(cipher=OpenABECipher())

    @given(pkcs=keys(), pku=keys(), attribute_expr=attributes())
    def test_returns_non_empty_key(self, pkcs, pku, attribute_expr):
        proxykey_user = self.key_gen.generate(pku, pkcs, attribute_expr)
        self.assertTrue(proxykey_user)

    @given(pkcs=keys(), pku=keys(), attribute_expr=attributes())
    def test_same_inputs_different_key(self, pkcs, pku, attribute_expr):
        proxykey_a = self.key_gen.generate(pku, pkcs, attribute_expr)
        proxykey_b = self.key_gen.generate(pku, pkcs, attribute_expr)
        self.assertNotEqual(proxykey_a, proxykey_b)

    @given(pkcs=keys(), pku=keys(), attribute_expr=attributes())
    def test_key_meets_key_spec(self, pkcs, pku, attribute_expr):
        proxy_key = self.key_gen.generate(pku, pkcs, attribute_expr)
        assert_valid(proxy_key)


if __name__ == '__main__':
    unittest.main()
