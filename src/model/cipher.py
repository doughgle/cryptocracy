from charm.schemes.abenc.abenc_yllc15 import YLLC15
from charm.toolbox.pairinggroup import PairingGroup


class NullCipher(object):

    def setup(self):
        raise NotImplementedError

    def user_keygen(self, pk, mk, object):
        raise NotImplementedError

    def proxy_keygen(self, cloud_server_public_key,
                     user_public_key,
                     user_id,
                     attribute_list):
        raise NotImplementedError

    def encrypt(self, plaintext, policy_expression):
        raise NotImplementedError

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, user_id, ciphertext):
        return "intermediate_value"

    def decrypt(self, user_private_key, intermediate_value):
        raise NotImplementedError


class CharmABE(object):

    def __init__(self):
        group = PairingGroup('SS512')
        self.abe = YLLC15(group)

    def setup(self):
        pass

    def user_keygen(self, pk, mk, object):
        raise NotImplementedError

    def proxy_keygen(self, cloud_server_public_key,
                     user_public_key,
                     user_id,
                     attribute_list):
        raise NotImplementedError

    def encrypt(self, plaintext, policy_expression):
        raise NotImplementedError

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, user_id, ciphertext):
        return "intermediate_value"

    def decrypt(self, user_private_key, intermediate_value):
        raise NotImplementedError