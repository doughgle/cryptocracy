from src.model.result import RESULT


class EncryptFileUseCase(object):
    def __init__(self, cipher):
        self.cipher = cipher

    def run(self, request):
        result = RESULT.FAILURE
        try:
            with open(request.input_file, 'r') as in_f:
                plaintext = in_f.read()
            ciphertext = self.cipher.encrypt(plaintext,
                                             request.policy_expression)
            with open(request.output_file, 'w') as out_f:
                out_f.write(ciphertext)
            result = RESULT.SUCCESS
        finally:
            response = EncryptFileResponse(result,
                                           request.output_file)
        return response


class EncryptFileRequest(object):
    def __init__(self, input_file, policy_expression, output_file=None):
        self._input_file = input_file
        self._policy_expression = policy_expression
        self._output_file = output_file if output_file is not None else input_file

    @property
    def input_file(self):
        return self._input_file

    @property
    def output_file(self):
        return self._output_file

    @property
    def policy_expression(self):
        return self._policy_expression


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
