import os
import unittest

from src.model.result import RESULT
from src.use_cases.upload_file import UploadFileUseCase, UploadFileRequest, UploadFileResponse


class UploadFileTest(unittest.TestCase):

    def setUp(self):
        self.input_file = os.path.join(os.path.dirname(__file__), 'cipher.txt')
        with open(self.input_file, 'w') as f:
            f.write("49879ad8a9360fc==")

    def tearDown(self):
        os.remove(self.input_file)

    def test_upload_existing_file_to_default_location(self):
        upload_file = UploadFileUseCase()
        response = upload_file.run(UploadFileRequest(self.input_file))

        expected_response = UploadFileResponse(
            result=RESULT.SUCCESS,
            url='cipher.txt'
        )
        self.assertEqual(expected_response, response)
