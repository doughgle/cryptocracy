from src.model.cipher import NullCipher


class ProxyKeyGenerator(object):

    def __init__(self, cipher=NullCipher()):
        self.cipher = cipher

    def generate(self, user_public_key, cloud_server_public_key, user_attributes):
        user_id = user_public_key
        return self.cipher.proxy_keygen(cloud_server_public_key,
                     user_public_key,
                     user_id,
                     user_attributes)
