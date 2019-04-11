from src.model.result import RESULT


class EncryptFileUseCase(object):
    def __init__(self, abe_scheme):
        self.abe_scheme = abe_scheme

    def run(self, request):
        result = RESULT.FAILURE
        try:
            with open(request.input_file, 'rb') as in_f:
                plaintext = in_f.read()
            ciphertext = self.abe_scheme.encrypt(request.params,
                                                 plaintext,
                                                 request.policy_expression)
            with open(request.output_file, 'wb') as out_f:
                out_f.write(ciphertext)
            result = RESULT.SUCCESS
        finally:
            response = EncryptFileResponse(result,
                                           request.output_file)
        return response


class EncryptFileRequest(object):
    def __init__(self, input_file, policy_expression, output_file, params):
        self._input_file = input_file
        self._policy_expression = policy_expression
        self._output_file = output_file if output_file is not None else input_file
        self._params = params

    @property
    def input_file(self):
        return self._input_file

    @property
    def output_file(self):
        return self._output_file

    @property
    def policy_expression(self):
        return self._policy_expression

    @property
    def params(self):
        return self._params


class EncryptFileResponse(dict):
    def __init__(self, result, output_file):
        super(EncryptFileResponse, self).__init__({"result": result,
                                                   "output_file": output_file})

    @property
    def result(self):
        return self.__getitem__("result")

    @property
    def output_file(self):
        return self.__getitem__("output_file")
