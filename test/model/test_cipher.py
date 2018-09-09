import unittest

import simplecrypt
from hypothesis import given, settings
from hypothesis.strategies import binary

from src.model.key_spec import keys
from src.model.policy_expression_spec import policy_expressions


class Cipher(object):
    def encrypt(self, plaintext, policy_expression):
        return simplecrypt.encrypt(u'vigenere', plaintext)

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, ciphertext):
        return ciphertext

    def decrypt(self, user_private_key, intermediate_value):
        return simplecrypt.decrypt(u'vigenere', intermediate_value)


class TestCipher(unittest.TestCase):

    @settings(max_examples=3)
    @given(binary(), policy_expressions())
    def test_ciphertext_is_never_equal_to_plaintext(self, plaintext, policy_expression):
        cipher = Cipher()
        ciphertext = cipher.encrypt(plaintext, policy_expression)
        assert ciphertext != plaintext

    @settings(max_examples=3)
    @given(plaintext=binary(),
           cloud_server_private_key=keys(),
           proxy_key_user=keys(),
           user_private_key=keys(),
           policy_expression=policy_expressions())
    def test_encrypt_proxy_decrypt_decrypt_round_trip(self,
                                                      plaintext,
                                                      cloud_server_private_key,
                                                      proxy_key_user,
                                                      user_private_key,
                                                      policy_expression):
        cipher = Cipher()

        ciphertext = cipher.encrypt(plaintext, policy_expression)
        intermediate_value = cipher.proxy_decrypt(cloud_server_private_key, proxy_key_user, ciphertext)
        assert plaintext == cipher.decrypt(user_private_key, intermediate_value)
