import os
import unittest

from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.result import RESULT
from src.use_cases.download_file import DownloadFileUseCase, DownloadFileRequest


class DownloadFileTest(unittest.TestCase):

    def setUp(self):
        self.input_file = os.path.join(os.path.dirname(__file__), 'cipher.txt')
        self.proxy_key_store = ProxyKeyStore()
        self.proxy_key_store.put("alice@dev.net", "7a9360fc945435a33==")

        with open(self.input_file, 'w') as f:
            f.write("4d916ac7a9360fc==")

        self.download_file = DownloadFileUseCase(self.proxy_key_store)

    def tearDown(self):
        os.remove(self.input_file)

    def test_download_existing_file(self):
        request = DownloadFileRequest("alice@dev.net", "file://" + self.input_file)

        response = self.download_file.run(request)

        self.assertEqual(RESULT.SUCCESS, response.result)
        self.assertEqual("http://proxy-crypt/file/945435a339729aa4b4d916ac7a9360fc", response.download_url)

    def test_proxy_key_not_found(self):
        request = DownloadFileRequest("bob@dev.net", "file://" + self.input_file)

        response = self.download_file.run(request)

        self.assertEqual(RESULT.FAILURE, response.result)
        self.assertEqual(None, response.download_url)
