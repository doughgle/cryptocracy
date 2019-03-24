import unittest

from hypothesis import given

from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.abe_scheme import NullCipher
from src.model.key_spec import keys
from src.model.result import RESULT
from src.use_cases.add_user import AddUserRequest
from src.use_cases.add_user import AddUserUseCase


class AddUserTest(unittest.TestCase):

    @given(user_public_key=keys())
    def test_add_user_stores_proxy_key(self, user_public_key):
        proxy_key_store = ProxyKeyStore()
        abe_scheme = FakeProxyKeyABE()
        add_user = AddUserUseCase(abe_scheme, proxy_key_store)

        user_id = "alice.tan@nus.edu.sg"
        attributes = {"gender": "female", "age": 25}
        request = AddUserRequest(user_id, user_public_key, attributes)

        response = add_user.run(request)

        self.assertEqual(
            "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f",
            proxy_key_store.get(user_id)
        )
        
        self.assertDictEqual({"result": RESULT.SUCCESS, "user_id": user_id}, response)


class FakeProxyKeyABE(NullCipher):

    def proxy_keygen(self, cloud_server_public_key, user_public_key, user_id, attribute_list):
        return "dc5819e1ae1450c6044a9cc3dacc896b9d09d12f"


if __name__ == '__main__':
    unittest.main()
