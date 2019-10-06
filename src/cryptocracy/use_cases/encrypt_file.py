from cryptocracy.model.result import RESULT, STATUS


class EncryptFileUseCase(object):
    def __init__(self, abe_scheme):
        self.abe_scheme = abe_scheme

    def run(self, request):
        result = RESULT.FAILURE

        if request.output_file == request.input_file and not request.encrypt_in_place:
            return EncryptFileResponse(result,
                                       request.output_file,
                                       status=STATUS.WARNING,
                                       message='Input file will be encrypted in-place! '
                                               'This may not be what you intended. '
                                               'Note that to decrypt the ciphertext, '
                                               'the cloud must perform a proxy-decrypt operation '
                                               "using the user's proxy key and the cloud server's private key."
                                       )

        try:
            with open(request.input_file, 'rb') as in_f:
                plaintext = in_f.read()
            ciphertext = self.abe_scheme.encrypt(request.params,
                                                 plaintext,
                                                 request.read_policy_expression)
            with open(request.output_file, 'wb') as out_f:
                out_f.write(ciphertext)
            result = RESULT.SUCCESS
        finally:
            response = EncryptFileResponse(result,
                                           request.output_file
                                           )
        return response


class EncryptFileRequest(object):
    def __init__(self, input_file, read_policy_expression, output_file, params, encrypt_in_place=False):
        self._input_file = input_file
        self._read_policy_expression = read_policy_expression
        self._output_file = output_file
        self._params = params
        self._encrypt_in_place = encrypt_in_place

    @property
    def input_file(self):
        return self._input_file

    @property
    def output_file(self):
        return self._output_file

    @property
    def read_policy_expression(self):
        return self._read_policy_expression

    @property
    def params(self):
        return self._params

    @property
    def encrypt_in_place(self):
        return self._encrypt_in_place


class EncryptFileResponse(dict):
    def __init__(self, result, output_file, status=STATUS.OK, message=None):
        super(EncryptFileResponse, self).__init__({"result": result,
                                                   "output_file": output_file,
                                                   "status": status,
                                                   "message": message
                                                   })

    @property
    def result(self):
        return self.__getitem__("result")

    @property
    def output_file(self):
        return self.__getitem__("output_file")

    @property
    def status(self):
        return self.__getitem__("status")

    @property
    def message(self):
        return self.__getitem__("message")
