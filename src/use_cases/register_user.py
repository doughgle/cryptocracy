from src.model.key_spec import assert_valid as assert_valid_key
from src.model.result import RESULT
from src.model.user_id import assert_valid as assert_valid_user_id


class RegisterUserUseCase(object):
    def __init__(self, ka_service):
        """
        :type ka_service: KeyAuthorityService
        """
        self.ka_service = ka_service

    def run(self, request):
        """
        :type request: RegisterUserRequest
        :return response: RegisterUserResponse
        """
        register_response = self.ka_service.register(request.user_id, request.user_public_key)
        error = register_response['error']
        result = RESULT.SUCCESS if error is None else RESULT.FAILURE
        response = {"result": result}
        response.update(register_response)
        return RegisterUserResponse(response)


class RegisterUserRequest(dict):

    def __init__(self, user_id, pku_b64):
        """
        :param user_id: the user identifier
        :param pku_b64: the base64-encoded user public key

        base64 bytes are decoded into UTF-8 on construction in accordance with best practices.
        Here, `user_public_key` is used to represent UTF-8-encoded string for processing.
        https://unicodebook.readthedocs.io/good_practices.html
        """
        assert_valid_user_id(user_id)
        assert_valid_key(pku_b64)
        super(RegisterUserRequest, self).__init__({"user_id": user_id,
                                                   "user_public_key": pku_b64.decode('UTF-8')})

    @property
    def user_id(self):
        return self.__getitem__("user_id")

    @property
    def user_public_key(self):
        """
        :return: a UTF-8 encoded string which can be used in JSON
        """
        return self.__getitem__("user_public_key")


class RegisterUserResponse(dict):
    pass