import unittest

from hypothesis import given, settings
from hypothesis._strategies import lists
from hypothesis.strategies import binary, emails

from cryptocracy.model.abe_scheme import CharmHybridABE as ABE
from cryptocracy.model.policy_expression_spec import attributes


class TestCipher(unittest.TestCase):

    @settings(max_examples=30, deadline=None)
    @given(plaintext=binary(min_size=1),
           user_id=emails(),
           attribute_list=lists(attributes(), min_size=1))
    def test_correctness(self,
                         plaintext,
                         user_id,
                         attribute_list):
        abe = ABE()
        params, msk = abe.setup()

        pku, sku = abe.user_keygen(params)
        pkcs, skcs = abe.user_keygen(params)
        proxy_key_user = abe.proxy_keygen(msk, params, pkcs, pku, attribute_list)
        policy_expression = attribute_list[0]

        pt = str(plaintext, 'latin-1')
        ciphertext = abe.encrypt(params, pt, policy_expression)
        intermediate_value = abe.proxy_decrypt(skcs, proxy_key_user, ciphertext)
        self.assertEqual(pt, str(abe.decrypt(sku, intermediate_value), 'utf8'))