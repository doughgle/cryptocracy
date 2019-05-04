import json

import requests

from src.model import key_spec, user_id
from src.model.exceptions import InvalidInput
from src.model.result import RESULT


class AddUserUseCase(object):
    def __init__(self, client, abe_scheme, proxy_key_store, server_address='localhost:5000'):
        """
        :type client: requests
        :param abe_scheme: an ABE scheme that supports proxy_keygen
        :param proxy_key_store: key-value store for user proxy keys
        :param server_address: hostname<:port>
        """
        self.server_address = server_address
        self.abe_scheme = abe_scheme
        self.proxy_key_store = proxy_key_store
        self.client = client

    def run(self, request):
        """
        :type request: AddUserRequest
        :return: response: result and user_id
        """
        try:
            user_id.assert_valid(request.user_id)
            # retrieve user_public_key for user_id
            http_response = self.client.get('http://%s/user/%s' % (self.server_address, request.user_id),
                                            json={"user_id": request.user_id}
                                            )
            if http_response.status_code == 404:
                raise InvalidInput("User (%s) not found" % request.user_id)

            user_public_key = http_response.json()['user_public_key']
            key_spec.assert_valid(user_public_key)

            # retrieve cloud_server_public_key for cloud
            cs_id = "cryptocracy@amazonaws.com"
            http_response = self.client.get('http://%s/user/%s' % (self.server_address, cs_id),
                                            json={"user_id": cs_id}
                                            )
            if http_response.status_code == 404:
                raise InvalidInput("User (%s) not found" % cs_id)

            pkcs = http_response.json()['user_public_key']
            key_spec.assert_valid(pkcs)

            proxy_key = self.abe_scheme.proxy_keygen(pkcs,
                                                     user_public_key,
                                                     request.attributes)
            key_spec.assert_valid(proxy_key)
            self.proxy_key_store.put(request.user_id, proxy_key)
            return {"result": RESULT.SUCCESS, "user_id": request.user_id}
        except InvalidInput as e:
            return {"result": RESULT.FAILURE, "user_id": request.user_id, "error": e.message}


class AddUserRequest(object):
    def __init__(self, user_id, attributes):
        """
        :type attributes: str
        """
        self._user_id = user_id
        self._attributes = json.loads(attributes)

    @property
    def user_id(self):
        return self._user_id

    @property
    def attributes(self):
        return self._attributes
