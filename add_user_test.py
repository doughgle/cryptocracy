import unittest

class AddUserTest(unittest.TestCase):
    def runTest(self):
        user_id = "123456" # Alice Tan
        attributes = {"gender" : "female", "age" : 25}
        user_public_key = "bfed8adb4f21cc3f2a813ed8389d02709f34749f"
        cloud_server = CloudServerMock()
        proxy_key_gen = ProxyKeyGeneratorMock()

        add_user = AddUserUseCase(proxy_key_gen, cloud_server)
        add_user.run(user_id, user_public_key, attributes)

        self.assertIn(user_id, cloud_server.get_proxy_key_store())
        self.assertEqual(
            "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f",
            cloud_server.get_proxy_key(user_id))

class AddUserUseCase(object):
    def __init__(self, proxy_key_gen, cloud_server):
        self.proxy_key_gen = proxy_key_gen
        self.cloud_server = cloud_server

    def run(self, user_id, user_public_key, attributes):
        proxy_key = self.proxy_key_gen.generate()
        self.cloud_server.add_user_proxy_key(user_id, proxy_key)

class CloudServerMock(object):

    def __init__(self):
        self.proxy_key_store = {}

    def add_user_proxy_key(self, user_id, proxy_key):
        self.proxy_key_store[user_id] = proxy_key

    def get_proxy_key(self, user_id):
        return self.proxy_key_store[user_id]

    def get_proxy_key_store(self):
        '''spy method'''
        return self.proxy_key_store

class ProxyKeyGeneratorMock(object):

    def generate(self):
        return "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f"

if __name__ == '__main__':
    unittest.main()
