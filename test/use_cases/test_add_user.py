import unittest

from hypothesis import given

from src.boundaries.proxy_key_store import ProxyKeyStore
from src.use_cases.add_user import AddUserUseCase
from src.model.key_spec import keys
from src.model.result import RESULT
from src.use_cases.add_user import AddUserRequest


class AddUserTest(unittest.TestCase):

    @given(user_public_key=keys())
    def runTest(self, user_public_key):
        proxy_key_store = ProxyKeyStore()
        proxy_key_gen = ProxyKeyGeneratorMock()
        add_user = AddUserUseCase(proxy_key_gen, proxy_key_store)

        user_id = "alice.tan@nus.edu.sg"
        attributes = {"gender": "female", "age": 25}
        request = AddUserRequest(user_id, user_public_key, attributes)

        response = add_user.run(request)

        self.assertEqual(
            "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f",
            proxy_key_store.get(user_id)
        )
        
        self.assertDictContainsSubset({"result": RESULT.SUCCESS, "user_id": user_id}, response)


class ProxyKeyGeneratorMock(object):

    def generate(self, user_public_key, cloud_server_public_key, user_attributes):
        return "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f"


if __name__ == '__main__':
    unittest.main()
