import unittest

from src.use_cases.encrypt_file import EncryptFileResponse, EncryptFileUseCase, EncryptFileRequest
from src.use_cases.result import RESULT


class NullCipher(object):
    def encrypt(self, input_file, output_file, policy_expression):
        return True


class EncryptFileTest(unittest.TestCase):
    def test_encrypt_to_output_file(self):
        encrypt_file = EncryptFileUseCase(cipher=NullCipher())
        request = EncryptFileRequest(input_file='message.txt',
                                     policy_expression='',
                                     output_file='cipher.txt')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(RESULT.SUCCESS, 'cipher.txt')
        self.assertEqual(expected_response, response)

    def test_encrypt_file_in_place(self):
        encrypt_file = EncryptFileUseCase(cipher=NullCipher())
        request = EncryptFileRequest(input_file='vault.yml', policy_expression='')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(result=RESULT.SUCCESS, output_file='vault.yml')
        self.assertEqual(expected_response, response)


