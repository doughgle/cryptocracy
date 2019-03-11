import unittest

from hypothesis import given, settings
from hypothesis._strategies import lists
from hypothesis.strategies import binary, emails

from src.model.cipher import CharmABE as Cipher
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
        cipher = Cipher()
        cipher.setup()

        pku, sku = cipher.user_keygen(user_id)
        pkcs, skcs = cipher.user_keygen(user_id)
        proxy_key_user = cipher.proxy_keygen(pkcs, pku, user_id, attribute_list)
        policy_expression = attribute_list[0]

        pt = str(plaintext, 'latin-1')
        ciphertext = cipher.encrypt(pt, policy_expression)
        intermediate_value = cipher.proxy_decrypt(skcs, proxy_key_user, user_id, ciphertext)
        self.assertEqual(pt, str(cipher.decrypt(sku, intermediate_value), 'utf8'))

    @given(binary(min_size=1), policy_expressions())
    def test_ciphertext_is_never_equal_to_plaintext(self, plaintext, policy_expression):
        cipher = Cipher()
        cipher.setup()
        pt = str(plaintext, 'latin-1')
        ciphertext = cipher.encrypt(pt, policy_expression)
        assert ciphertext != plaintext
