import os
import unittest

from hypothesis.strategies import binary
from hypothesis import given, settings

from src.boundaries.object_store import ObjectStore, AwsObjectStore


class ObjectStoreTest(unittest.TestCase):

    def __init__(self, methodName, object_store=ObjectStore()):
        self.store = object_store
        unittest.TestCase.__init__(self, methodName)

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), 'cipher.txt')

    def tearDown(self):
        os.remove(self.path)

    @settings(max_examples=3)
    @given(ciphertext=binary(min_size=16, max_size=2048))
    def test_put_get_round_trip(self, ciphertext):
        with open(self.path, 'wb') as f:
            f.write(ciphertext)

        key = os.path.basename(self.path)
        self.store.put(self.path, key)
        download_url = self.store.get_download_url(key)
        data = self.store.get(download_url)
        self.assertEquals(ciphertext, data)
        self.store.delete(key)


class AwsObjectStoreTest(ObjectStoreTest):

    def __init__(self, methodName):
        ObjectStoreTest.__init__(self, methodName, object_store=AwsObjectStore(u'proxy-crypt-bucket-nonprod'))
