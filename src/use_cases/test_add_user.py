import unittest
from add_user import AddUserUseCase
from add_user import Result
from add_user import AddUserRequest


class AddUserTest(unittest.TestCase):
    def runTest(self):
        user_id = "123456" # Alice Tan
        attributes = {"gender" : "female", "age" : 25}
        user_public_key = "bfed8adb4f21cc3f2a813ed8389d02709f34749f"
        cloud_server = CloudServerMock()
        proxy_key_gen = ProxyKeyGeneratorMock()

        add_user = AddUserUseCase(proxy_key_gen, cloud_server)
        request = AddUserRequest(user_id, user_public_key, attributes)
        response = add_user.run(request)

        self.assertIn(user_id, cloud_server.get_proxy_key_store())
        self.assertEqual(
            "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f",
            cloud_server.get_proxy_key(user_id)
        )
        
        self.assertDictContainsSubset({"result": Result.SUCCESS, "user_id": 800800}, response)

class CloudServerMock(object):

    @property
    def public_key(self):
        return '4228e3eabc0ec5d246ef114eb0c11edbe6453190'

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

    def generate(self, user_public_key, cloud_server_public_key, user_attributes):
        return "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f"

if __name__ == '__main__':
    unittest.main()
