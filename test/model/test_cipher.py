import unittest

from hypothesis import given, settings
from hypothesis.strategies import binary, emails

from src.model.cipher import OpenABECipher
from src.model.key_spec import keys
from src.model.policy_expression_spec import policy_expressions, attributes


class TestCipher(unittest.TestCase):

    @settings(max_examples=30)
    @given(plaintext=binary(min_size=1),
           cloud_server_private_key=keys(),
           cloud_server_public_key=keys(),
           proxy_key_user=keys(),
           user_private_key=keys(),
           user_public_key=keys(),
           user_id=emails(),
           attribute=attributes())
    def test_encrypt_proxy_decrypt_decrypt_round_trip(self,
                                                      plaintext,
                                                      cloud_server_public_key,
                                                      cloud_server_private_key,
                                                      proxy_key_user,
                                                      user_public_key,
                                                      user_private_key,
                                                      user_id,
                                                      attribute):
        cipher = OpenABECipher()
        cipher.proxy_keygen(cloud_server_public_key, user_public_key, user_id, attribute)
        policy_expression = attribute

        pt = unicode(plaintext, 'latin-1')
        ciphertext = cipher.encrypt(pt, policy_expression)
        intermediate_value = cipher.proxy_decrypt(cloud_server_private_key, proxy_key_user, user_id, ciphertext)
        self.assertEqual(pt, unicode(cipher.decrypt(user_private_key, intermediate_value), 'utf8'))

    @given(binary(min_size=1), policy_expressions())
    def test_ciphertext_is_never_equal_to_plaintext(self, plaintext, policy_expression):
        cipher = OpenABECipher()
        pt = unicode(plaintext, 'latin-1')
        ciphertext = cipher.encrypt(pt, policy_expression)
        assert ciphertext != plaintext
