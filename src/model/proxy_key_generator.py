import os


class ProxyKeyGenerator(object):

    def __init__(self, master_secret_key):
        pass

    def generate(self, user_public_key, cloud_server_public_key, user_attributes):
        return os.urandom(10)
