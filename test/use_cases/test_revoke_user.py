import unittest

from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.result import RESULT


class RevokeUserResponse(dict):
    pass
    # def __init__(self):
    #     super(RevokeUserResponse, self).__init__({"result": RESULT.SUCCESS, "user_id": "id"})


class RevokeUserUseCase(object):
    def __init__(self, proxy_key_store):
        self.proxy_key_store = proxy_key_store

    def run(self, request):
        try:
            self.proxy_key_store.delete(request.user_id)
            return RevokeUserResponse({"result": RESULT.SUCCESS, "user_id": request.user_id})
        except KeyError:
            return RevokeUserResponse({"result": RESULT.FAILURE, "user_id": request.user_id, "error": "does not exist"})


class RevokeUserRequest(object):
    def __init__(self, user_id):
        self._user_id = user_id

    @property
    def user_id(self):
        return self._user_id


class RevokeUserTest(unittest.TestCase):

    def test_revoke_existing_user(self):
        proxy_key_store = ProxyKeyStore()
        user_id = "alice.tan@nus.edu.sg"
        proxy_key = "IKUCwiMT5X1CruqyabR13Q=="
        proxy_key_store.put(user_id, proxy_key)
        revoke_user = RevokeUserUseCase(proxy_key_store)
        request = RevokeUserRequest(user_id)

        response = revoke_user.run(request)

        self.assertRaises(KeyError, proxy_key_store.get, user_id)
        self.assertDictContainsSubset({"result": RESULT.SUCCESS, "user_id": user_id}, response)

    def test_revoke_non_existing_user(self):
        proxy_key_store = ProxyKeyStore()
        user_id = "alice.tan@nus.edu.sg"
        revoke_user = RevokeUserUseCase(proxy_key_store)
        request = RevokeUserRequest(user_id)

        response = revoke_user.run(request)

        self.assertDictContainsSubset({"result": RESULT.FAILURE, "user_id": user_id, "error": "does not exist"}, response)


if __name__ == '__main__':
    unittest.main()
