import unittest

from hypothesis import given, settings
from hypothesis._strategies import lists
from hypothesis.strategies import binary, emails

from src.model.abe_scheme import CharmHybridABE as ABE
from src.model.policy_expression_spec import policy_expressions, attributes


class TestCipher(unittest.TestCase):

    @settings(max_examples=30, deadline=350)
    @given(plaintext=binary(min_size=1),
           user_id=emails(),
           attribute_list=lists(attributes(), min_size=1))
    def test_encrypt_proxy_decrypt_decrypt_round_trip(self,
                                                      plaintext,
                                                      user_id,
                                                      attribute_list):
        abe = ABE()
        abe.setup()

        pku, sku = abe.user_keygen(user_id)
        pkcs, skcs = abe.user_keygen(user_id)
        proxy_key_user = abe.proxy_keygen(pkcs, pku, user_id, attribute_list)
        policy_expression = attribute_list[0]

        pt = str(plaintext, 'latin-1')
        ciphertext = abe.encrypt(pt, policy_expression)
        intermediate_value = abe.proxy_decrypt(skcs, proxy_key_user, user_id, ciphertext)
        self.assertEqual(pt, str(abe.decrypt(sku, intermediate_value), 'utf8'))

    @given(binary(min_size=1), policy_expressions())
    def test_ciphertext_is_never_equal_to_plaintext(self, plaintext, policy_expression):
        abe = ABE()
        abe.setup()
        pt = str(plaintext, 'latin-1')
        ciphertext = abe.encrypt(pt, policy_expression)
        assert ciphertext != plaintext
