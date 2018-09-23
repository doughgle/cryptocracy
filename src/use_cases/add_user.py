from src.model.result import RESULT


class AddUserUseCase(object):
    def __init__(self, proxy_key_gen, cloud_server):
        self.proxy_key_gen = proxy_key_gen
        self.cloud_server = cloud_server

    def run(self, request):
        '''
        :type request: AddUserRequest
        :return: response: result and user_id
        '''
        proxy_key = self.proxy_key_gen.generate(
            request.user_public_key,
            self.cloud_server.public_key,
            request.attributes
        )
        self.cloud_server.put(request.user_id, proxy_key)
        return {"result": RESULT.SUCCESS, "user_id": request.user_id}


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