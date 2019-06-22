import os
import unittest

from cryptocracy.model.result import RESULT
from cryptocracy.use_cases.encrypt_file import EncryptFileResponse, EncryptFileUseCase, EncryptFileRequest


class NullAbeScheme(object):
    def encrypt(self, params, plaintext, policy_expression):
        ciphertext = b'ciphertext'
        return ciphertext


class EncryptFileTest(unittest.TestCase):

    def setUp(self):
        self.input_file = os.path.join(os.path.dirname(__file__), 'message.txt')
        self.output_file = 'cipher.txt'

        with open(self.input_file, 'w') as f:
            f.write("hello crypto world")

    def tearDown(self):
        os.remove(self.input_file)

    def test_encrypt_to_output_file(self):
        encrypt_file = EncryptFileUseCase(abe_scheme=NullAbeScheme())
        request = EncryptFileRequest(self.input_file,
                                     policy_expression=u'((Manager and Experience > 3) or Admin)',
                                     output_file=self.output_file,
                                     params=b'public scheme params')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(RESULT.SUCCESS, self.output_file)
        self.assertEqual(expected_response, response)
        os.remove(self.output_file)