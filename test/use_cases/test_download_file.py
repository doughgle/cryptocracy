import os
import unittest

from src.boundaries.object_store import ObjectStore
from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.cipher import OpenABECipher
from src.model.result import RESULT, STATUS
from src.use_cases.download_file import DownloadFileUseCase, DownloadFileRequest, DownloadFileResponse


class DownloadFileTest(unittest.TestCase):

    def setUp(self):
        cipher = OpenABECipher()
        # key authority adds user
        alice = "alice@dev.net"
        alice_key = cipher.proxy_keygen("", "", user_id=alice, attribute_list="Singaporean|female")

        proxy_key_store = ProxyKeyStore()
        proxy_key_store.put(alice, alice_key)

        # data owner encrypts cyphertext
        ciphertext = cipher.encrypt("hello ABE world!", "Singaporean")
        self.input_file = os.path.join(os.path.dirname(__file__), 'cipher.txt')
        with open(self.input_file, 'wb') as f:
            f.write(ciphertext)

        # data owner uploads ciphertext to cloud storage
        obj_store = ObjectStore()
        key = os.path.basename(self.input_file)
        obj_store.put(self.input_file, key)
        self.download_url = obj_store.get_download_url(key)

        self.download_file = DownloadFileUseCase(proxy_key_store, obj_store, cipher=cipher)

    def tearDown(self):
        os.remove(self.input_file)

    def test_download_existing_file(self):
        request = DownloadFileRequest("alice@dev.net", self.download_url)

        response = self.download_file.run(request)

        expected_response = DownloadFileResponse(
            result=RESULT.SUCCESS,
            download_url='fca2b4fd8e90fc9537720c3d00b0fd37433fa33aec12c76a4a33255dab27a16a',
            content='hello ABE world!'
        )
        self.assertEqual(expected_response, response)

    def test_proxy_key_not_found(self):
        request = DownloadFileRequest("bob@dev.net", self.download_url)

        response = self.download_file.run(request)

        self.assertEqual(RESULT.FAILURE, response.result)
        self.assertEqual(STATUS.FORBIDDEN, response.status)
        self.assertEqual(None, response.download_url)

    def test_file_not_found(self):
        request = DownloadFileRequest("alice@dev.net", "file://" + "missing.me")

        response = self.download_file.run(request)

        self.assertEqual(RESULT.FAILURE, response.result)
        self.assertEqual(STATUS.NOT_FOUND, response.status)
        self.assertEqual(None, response.download_url)
