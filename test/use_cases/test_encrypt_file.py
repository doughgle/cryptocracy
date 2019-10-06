import os
import unittest

from cryptocracy.model.result import RESULT, STATUS
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
                                     read_policy_expression=u'((Manager and Experience > 3) or Admin)',
                                     output_file=self.output_file,
                                     params=b'public scheme params')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(RESULT.SUCCESS, self.output_file)
        self.assertEqual(expected_response, response)
        os.remove(self.output_file)

    def test_prevent_accident_encrypts_in_place(self):
        encrypt_file = EncryptFileUseCase(abe_scheme=NullAbeScheme())
        request = EncryptFileRequest(self.input_file,
                                     read_policy_expression=u'(Human or Earthling)',
                                     output_file=self.input_file,
                                     params=b'public scheme params')
        response = encrypt_file.run(request)
        expected_response = EncryptFileResponse(RESULT.FAILURE,
                                                self.input_file,
                                                status=STATUS.WARNING,
                                                message='Input file will be encrypted in-place! '
                                                        'This may not be what you intended. '
                                                        'Note that to decrypt the ciphertext, '
                                                        'the cloud must perform a proxy-decrypt operation '
                                                        "using the user's proxy key and the cloud server's private key."
                                                )
        self.assertEqual(expected_response, response)
