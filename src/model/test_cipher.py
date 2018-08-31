import unittest

from hypothesis import given
from hypothesis.strategies import binary


class Cipher(object):
    def encrypt(self, message, policy_expression):
        return message

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, ciphertext):
        return ciphertext

    def decrypt(self, user_private_key, intermediate_value):
        return intermediate_value


class TestCipher(unittest.TestCase):

    @given(message=binary())
    def test_encrypt_decrypt_round_trip(self, message):
        cipher = Cipher()
        policy_expression = u'((Manager and Experience > 3) or Admin)'
        cloud_server_private_key = 'kashdkjahd'
        proxy_key_user = 'aksljnd09'
        user_private_key = 'ajsdknbcvcryto'

        ciphertext = cipher.encrypt(message, policy_expression)
        intermediate_value = cipher.proxy_decrypt(cloud_server_private_key, proxy_key_user, ciphertext)
        self.assertEqual(message, cipher.decrypt(user_private_key, intermediate_value))

