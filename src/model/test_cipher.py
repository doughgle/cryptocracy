import unittest

from hypothesis import given
from hypothesis.strategies import binary

from src.model.key_spec import keys
from src.model.policy_expression_spec import policy_expressions


class Cipher(object):
    def encrypt(self, message, policy_expression):
        return message

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, ciphertext):
        return ciphertext

    def decrypt(self, user_private_key, intermediate_value):
        return intermediate_value


class TestCipher(unittest.TestCase):

    @given(message=binary(),
           cloud_server_private_key=keys,
           proxy_key_user=keys,
           user_private_key=keys,
           policy_expression=policy_expressions())
    def test_encrypt_proxy_decrypt_decrypt_round_trip(self,
                                                      message,
                                                      cloud_server_private_key,
                                                      proxy_key_user,
                                                      user_private_key,
                                                      policy_expression):
        cipher = Cipher()

        ciphertext = cipher.encrypt(message, policy_expression)
        intermediate_value = cipher.proxy_decrypt(cloud_server_private_key, proxy_key_user, ciphertext)
        self.assertEqual(message, cipher.decrypt(user_private_key, intermediate_value))
