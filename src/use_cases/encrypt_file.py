from src.use_cases.result import RESULT


class EncryptFileUseCase(object):
    def __init__(self, cipher):
        self.cipher = cipher

    def run(self, request):
        result = self.cipher.encrypt(request.input_file,
                                     request.output_file,
                                     request.policy_expression)
        response = EncryptFileResponse(RESULT.SUCCESS if result else RESULT.FAILURE, request.output_file)
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


class EncryptFileResponse(object):
    def __init__(self, result, output_file):
        self._result = result
        self._output_file = output_file

    @property
    def result(self):
        return self._result

    @property
    def output_file(self):
        return self._output_file

    def __eq__(self, o):
        if not isinstance(o, EncryptFileResponse):
            return NotImplemented
        if self is o:
            return True
        return self.result == o.result and self.output_file == o.output_file

    def __repr__(self):
        return super(EncryptFileResponse, self).__repr__() + "result=" + self.result.name + "output_file=" + self.output_file
