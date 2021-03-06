import os
import unittest

from hypothesis import given, settings
from hypothesis.strategies import binary

from cryptocracy.boundaries.object_store import ObjectStore, AwsObjectStore
from cryptocracy.model.object_cache_lookup_key import lookup_keys


class ObjectStoreTest(unittest.TestCase):

    def __init__(self, methodName, object_store=ObjectStore()):
        self.store = object_store
        unittest.TestCase.__init__(self, methodName)

    @settings(max_examples=10, deadline=None)
    @given(ciphertext=binary(min_size=16, max_size=2048))
    def test_put_url_get_binary(self, ciphertext):
        self.path = os.path.join(os.path.dirname(__file__), 'cipher.txt')
        with open(self.path, 'wb') as f:
            f.write(ciphertext)

        key = os.path.basename(self.path)
        self.store.put(source_url=self.path, key=key)
        download_url = self.store.get_download_url(key)
        data = self.store.get(download_url)
        self.assertEqual(ciphertext, data)
        self.store.delete(key)
        os.remove(self.path)

    @settings(max_examples=10, deadline=None)
    @given(lookup_key=lookup_keys(), ciphertext=binary(min_size=16, max_size=2048))
    def test_put_binary_get_url(self, lookup_key, ciphertext):
        self.store.put_binary(lookup_key, ciphertext)
        download_url = self.store.get_download_url(lookup_key)
        downloaded_ciphertext = self.store.get(download_url)
        self.assertEqual(ciphertext, downloaded_ciphertext)


class AwsObjectStoreTest(ObjectStoreTest):

    def __init__(self, methodName):
        object_store_bucket_name = os.getenv('CRYPTOCRACY_OBJECT_STORE_BUCKET_NAME')
        ObjectStoreTest.__init__(self,
                                 methodName,
                                 object_store=AwsObjectStore(object_store_bucket_name))
