import unittest

from src.use_cases.result import RESULT


class EncryptFileUseCase(object):
    def run(self, request):
        return {"result": RESULT.SUCCESS,
                "output_file": 'cipher.txt'}


class EncryptFileRequest(object):
    def __init__(self, input_file, policy_expression, output_file=None):
        self._input_file = input_file
        self._policy_expression = policy_expression
        self._output_file = input_file


class EncryptFileTest(unittest.TestCase):
    def runTest(self):
        encrypt_file = EncryptFileUseCase()
        request = EncryptFileRequest(input_file='message.txt', policy_expression='', output_file='cipher.txt')
        response = encrypt_file.run(request)
        expected_response = {"result": RESULT.SUCCESS,
                             "output_file": 'cipher.txt'}
        self.assertEqual(expected_response, response)
