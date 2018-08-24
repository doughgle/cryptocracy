import unittest

from src.use_cases.encrypt_file import EncryptFileResponse, EncryptFileUseCase, EncryptFileRequest
from src.use_cases.result import RESULT


class NullCipher(object):
    def encrypt(self, input_file, output_file, policy_expression):
        pass


class EncryptFileTest(unittest.TestCase):
    def test_to_output_file(self):
        encrypt_file = EncryptFileUseCase(cipher=NullCipher())
        request = EncryptFileRequest(input_file='message.txt',
                                     policy_expression='',
                                     output_file='cipher.txt')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(RESULT.SUCCESS, 'cipher.txt')
        self.assertEqual(expected_response, response)
