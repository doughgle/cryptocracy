from src.model import key_spec
from src.model.exceptions import InvalidInput


class KeyAuthorityService(object):
    def __init__(self, client, server_address='localhost:5000'):
        """
        :type client: requests
        :param client:  HTTP client that implements the `requests` library API.
                        Specifically, `json()` for requests library Response.
        :param server_address: hostname<:port>
        """
        self.client = client
        self.server_address = server_address

    def get_public_key(self, uid):
        http_response = self.client.get('http://%s/user/%s' % (self.server_address, uid),
                                        json={"user_id": uid}
                                        )
        if http_response.status_code == 404:
            raise InvalidInput("User (%s) not found" % uid)
        public_key = http_response.json()['user_public_key']
        key_spec.assert_valid(public_key)
        return public_key

    def register(self, user_id, user_public_key):

        http_response = self.client.post("http://%s/register" % self.server_address,
                                         json={"user_id": user_id,
                                               "user_public_key": user_public_key}
                                         )
        return http_response.json()
