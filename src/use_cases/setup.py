from src.model.abe_scheme import NullCipher
from src.model.result import RESULT


class SetupUseCase(object):
    def __init__(self, abe_scheme=NullCipher()):
        self.abe = abe_scheme

    def run(self, request):
        """
        :type request: SetupRequest
        :return: response: SetupResponse
        """
        params, msk = self.abe.setup()
        return SetupResponse(RESULT.SUCCESS, params, msk)


class SetupRequest(object):
    def __init__(self):
        pass


class SetupResponse(dict):
    def __init__(self, result, params, msk):
        super(SetupResponse, self).__init__({"result": result, "params": params, "msk": msk})