import unittest

class AddUserTest(unittest.TestCase):
    def runTest(self):
        user_id = "123456" # Alice Tan
        attributes = {"gender" : "female", "age" : 25}
        user_public_key = "bfed8adb4f21cc3f2a813ed8389d02709f34749f"
        cloud_server = CloudServerMock()
        add_user = AddUserUseCase(cloud_server)
        add_user.run(user_id, user_public_key, attributes)
        self.assertIn(user_id, cloud_server.get_proxy_key_store())
        self.assertEqual(
            "273c1ff060399a9059558ff7e8d75876e36836d6",
            cloud_server.get_proxy_key(user_id))

class AddUserUseCase():
    def __init__(self, cloud_server):
        pass

    def run(self, user_id, user_public_key, attributes):
        pass

class CloudServerMock():

    def get_proxy_key_store(self):
        return {'123456': '273c1ff060399a9059558ff7e8d75876e36836d6'}

    def get_proxy_key(self, userid):
        return '273c1ff060399a9059558ff7e8d75876e36836d6'

if __name__ == '__main__':
    unittest.main()
