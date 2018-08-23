from enum import Enum

Result = Enum("Result", "SUCCESS FAILURE")

class AddUserUseCase(object):
    def __init__(self, proxy_key_gen, cloud_server):
        self.proxy_key_gen = proxy_key_gen
        self.cloud_server = cloud_server

    def run(self, user_id, user_public_key, attributes):
        proxy_key = self.proxy_key_gen.generate(
            user_public_key,
            self.cloud_server.public_key,
            attributes
        )
        self.cloud_server.add_user_proxy_key(user_id, proxy_key)
        return {"result": Result.SUCCESS, "user_id": 800800}


