import pyopenabe


class NullCipher(object):

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


class OpenABECipher(object):

    __openabe = pyopenabe.PyOpenABE()

    def __init__(self):
        self._cpabe = OpenABECipher.__openabe.CreateABEContext("CP-ABE")
        self._cpabe.generateParams()

    def user_keygen(self, pk, mk, object):
        raise NotImplementedError

    def proxy_keygen(self, cloud_server_public_key,
                     user_public_key,
                     user_id,
                     attribute_list):
        self._cpabe.keygen(attribute_list, user_id)

    def encrypt(self, plaintext, policy_expression):
        return self._cpabe.encrypt(policy_expression, plaintext)

    def proxy_decrypt(self, cloud_server_private_key, proxy_key_user, user_id, ciphertext):
        return self._cpabe.decrypt(user_id, ciphertext)

    def decrypt(self, user_private_key, intermediate_value):
        return intermediate_value