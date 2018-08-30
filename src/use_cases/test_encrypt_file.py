import unittest
import os

from src.use_cases.encrypt_file import EncryptFileResponse, EncryptFileUseCase, EncryptFileRequest
from src.use_cases.result import RESULT


class NullCipher(object):
    def encrypt(self, plaintext, policy_expression):
        ciphertext = 'ciphertext'
        return ciphertext


class FileOperatorMock(object):
    def open(self, input_file):
        pass


class EncryptFileTest(unittest.TestCase):

    def setUp(self):
        self.input_file = os.path.join(os.path.dirname(__file__), 'message.txt')
        self.output_file = 'cipher.txt'

        with open(self.input_file, 'w') as f:
            f.write("hello crypto world")

    def tearDown(self):
        os.remove(self.input_file)
        os.remove(self.output_file)

    def test_encrypt_to_output_file(self):
        encrypt_file = EncryptFileUseCase(cipher=NullCipher(), file_operator=FileOperatorMock())
        request = EncryptFileRequest(self.input_file,
                                     policy_expression='',
                                     output_file=self.output_file)
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(RESULT.SUCCESS, self.output_file)
        self.assertEqual(expected_response, response)

    def test_encrypt_file_in_place(self):
        encrypt_file = EncryptFileUseCase(cipher=NullCipher(), file_operator=FileOperatorMock())
        request = EncryptFileRequest(self.input_file, policy_expression='')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(result=RESULT.SUCCESS, output_file=self.input_file)
        self.assertEqual(expected_response, response)


