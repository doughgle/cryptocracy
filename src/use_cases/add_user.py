from src.model import key_spec, user_id
from src.model.result import RESULT
from src.model.user_id import InvalidInput


class AddUserUseCase(object):
    def __init__(self, proxy_key_gen, proxy_key_store):
        self.proxy_key_gen = proxy_key_gen
        self.proxy_key_store = proxy_key_store

    def run(self, request):
        '''
        :type request: AddUserRequest
        :return: response: result and user_id
        '''
        try:
            user_id.assert_valid(request.user_id)
            key_spec.assert_valid(request.user_public_key)
            proxy_key = self.proxy_key_gen.generate(
                request.user_public_key,
                self.proxy_key_store.public_key,
                request.attributes
            )
            self.proxy_key_store.put(request.user_id, proxy_key)
            return {"result": RESULT.SUCCESS, "user_id": request.user_id}
        except InvalidInput as e:
            return {"result": RESULT.FAILURE, "user_id": request.user_id, "error": e.message}


class AddUserRequest(object):
    def __init__(self, user_id, user_public_key, attributes):
        self._user_id = user_id
        self._user_public_key = user_public_key
        self._attributes = attributes

    @property
    def user_id(self):
        return self._user_id

    @property
    def user_public_key(self):
        return self._user_public_key

    @property
    def attributes(self):
        return self._attributes