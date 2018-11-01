import unittest

from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.result import RESULT
from src.use_cases.revoke_user import RevokeUserUseCase, RevokeUserRequest


class RevokeUserTest(unittest.TestCase):

    def setUp(self):
        self.proxy_key_store = ProxyKeyStore()

    def test_revoke_existing_user(self):
        user_id = "alice.tan@nus.edu.sg"
        proxy_key = "IKUCwiMT5X1CruqyabR13Q=="
        self.proxy_key_store.put(user_id, proxy_key)
        revoke_user = RevokeUserUseCase(self.proxy_key_store)
        request = RevokeUserRequest(user_id)

        response = revoke_user.run(request)

        self.assertRaises(KeyError, self.proxy_key_store.get, user_id)
        self.assertDictContainsSubset({"result": RESULT.SUCCESS, "user_id": user_id}, response)

    def test_revoke_non_existing_user(self):
        user_id = "alice.tan@nus.edu.sg"
        revoke_user = RevokeUserUseCase(self.proxy_key_store)
        request = RevokeUserRequest(user_id)

        response = revoke_user.run(request)

        self.assertDictContainsSubset({"result": RESULT.FAILURE, "user_id": user_id, "error": "does not exist"}, response)


if __name__ == '__main__':
    unittest.main()
