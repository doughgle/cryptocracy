from src.model.result import RESULT


class RevokeUserResponse(dict):
    pass


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