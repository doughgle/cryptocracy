from src.model.abe_scheme import DecryptionFailed
from src.model.result import RESULT, STATUS


class DecryptRequest(dict):
    def __init__(self, secret_key_b64, partial_ct_b64, output_file=None):
        super(DecryptRequest, self).__init__({"secret_key_b64": secret_key_b64,
                                              "partial_ct_b64": partial_ct_b64,
                                              "output_file": output_file})

    @property
    def secret_key_b64(self):
        return self.get("secret_key_b64")

    @property
    def partial_ct_b64(self):
        return self.get("partial_ct_b64")

    @property
    def output_file(self):
        return self.get("output_file")


class DecryptResponse(dict):
    def __init__(self, result, status, message='', output_file=None):
        super(DecryptResponse, self).__init__({"result": result,
                                               "status": status,
                                               "message": message,
                                               "output_file": output_file})


class DecryptUseCase(object):

    def __init__(self, abe_scheme):
        self.abe_scheme = abe_scheme

    def run(self, request):
        """
        :type request: DecryptRequest
        :rtype DecryptResponse
        """
        try:
            plaintext = self.abe_scheme.decrypt(request.secret_key_b64, request.partial_ct_b64)
            with open(request.output_file, 'wb') as out_f:
                out_f.write(plaintext)
            response = DecryptResponse(RESULT.SUCCESS, STATUS.OK, output_file=request.output_file)
        except (ValueError, DecryptionFailed) as e:
            response = DecryptResponse(RESULT.FAILURE, STATUS.FORBIDDEN, message=e.args[0])
        return response
