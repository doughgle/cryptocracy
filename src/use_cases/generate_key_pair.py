import os

from src.model.result import RESULT


class GenerateKeyPairUseCase(object):
    def __init__(self, abe_scheme):
        self.abe_scheme = abe_scheme

    def run(self, request):
        """
        :type request: GenerateKeyPairRequest
        """
        pk, sk = self.abe_scheme.user_keygen(request.params)
        with open(os.path.expandvars(request.public_key_file), 'wb') as pub:
            pub.write(pk)
        with open(os.path.expandvars(request.secret_key_file), 'wb') as key:
            key.write(sk)

        return {"result": RESULT.SUCCESS,
                "public_key_file": request.public_key_file,
                "public_key": pk,
                "secret_key_b64": request.secret_key_file,
                "secret_key": sk}


class GenerateKeyPairRequest(object):

    def __init__(self, params, public_key_file, secret_key_file):
        self._params = params
        self._public_key_file = public_key_file
        self._secret_key_file = secret_key_file

    @property
    def user_id(self):
        pass

    @property
    def params(self):
        return self._params

    @property
    def public_key_file(self):
        return self._public_key_file

    @property
    def secret_key_file(self):
        return self._secret_key_file

