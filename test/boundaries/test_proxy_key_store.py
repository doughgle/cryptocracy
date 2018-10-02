import unittest

from hypothesis import given, settings
from hypothesis.strategies import emails

from src.boundaries.proxy_key_store import ProxyKeyStore, AwsProxyKeyStore
from src.model.key_spec import keys


class InMemoryProxyKeyStoreTestBase(unittest.TestCase, object):

    def __init__(self, methodName, proxy_key_store=ProxyKeyStore()):
        self.proxy_key_store = proxy_key_store
        unittest.TestCase.__init__(self, methodName)

    @settings(max_examples=10)
    @given(user_id=emails(), proxy_key=keys())
    def test_add_key_for_userid_retrieve_by_userid(self, user_id, proxy_key):
        self.proxy_key_store.put(user_id, proxy_key)
        retrieved_key = self.proxy_key_store.get(user_id)
        self.assertEqual(proxy_key, retrieved_key)
        self.proxy_key_store.delete(user_id)


class AwsProxyKeyStoreTestBase(InMemoryProxyKeyStoreTestBase):

    def __init__(self, methodName):
        proxy_key_store = AwsProxyKeyStore(table_name=u'proxy-key-table-nonprod')
        InMemoryProxyKeyStoreTestBase.__init__(self, methodName, proxy_key_store)
