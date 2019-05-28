import json

from src.model import key_spec, user_id
from src.model.exceptions import InvalidInput
from src.model.result import RESULT


class AddUserUseCase(object):
    def __init__(self, ka_service, abe_scheme, proxy_key_store):
        """
        :param abe_scheme: an ABE scheme that supports proxy_keygen
        :param proxy_key_store: key-value store for user proxy keys
        """
        self.ka_service = ka_service
        self.abe_scheme = abe_scheme
        self.proxy_key_store = proxy_key_store

    def run(self, request):
        """
        :type request: AddUserRequest
        :return: response: result and user_id
        """
        uid = request.user_id
        try:
            key_spec.assert_valid(request.msk)
            key_spec.assert_valid(request.params)
            user_id.assert_valid(uid)
            # retrieve user_public_key for user_id
            pku = self.ka_service.get_public_key(uid)

            # retrieve cloud_server_public_key for cloud
            cs_id = "cryptocracy@amazonaws.com"
            pkcs = self.ka_service.get_public_key(cs_id)

            proxy_key = self.abe_scheme.proxy_keygen(request.msk, request.params, pkcs, pku, request.attributes)
            key_spec.assert_valid(proxy_key)
            self.proxy_key_store.put(uid, proxy_key)
            return {"result": RESULT.SUCCESS, "user_id": uid}
        except InvalidInput as e:
            return {"result": RESULT.FAILURE, "user_id": uid, "error": e.message}


class AddUserRequest(object):
    def __init__(self, msk, params, user_id, attributes):
        """
        :type attributes: str
        """
        self._msk = msk
        self._params = params
        self._user_id = user_id
        self._attributes = json.loads(attributes)

    @property
    def msk(self):
        return self._msk

    @property
    def params(self):
        return self._params

    @property
    def user_id(self):
        return self._user_id

    @property
    def attributes(self):
        return self._attributes
