from src.model.result import RESULT


class GenerateKeyPairUseCase(object):
    def __init__(self, abe_scheme):
        self.abe_scheme = abe_scheme

    def run(self, request):
        pk, sk = self.abe_scheme.user_keygen()
        return {"result": RESULT.SUCCESS, "public_key": pk, "secret_key": sk}


class GenerateKeyPairRequest(object):

    @property
    def user_id(self):
        pass