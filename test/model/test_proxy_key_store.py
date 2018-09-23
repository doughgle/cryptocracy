import unittest

from hypothesis import given, settings
from hypothesis.strategies import emails

from src.model.proxy_key_store import ProxyKeyStore, AwsProxyKeyStore
from src.model.key_spec import keys


class ProxyKeyStoreTestBase:

    @settings(max_examples=10)
    @given(user_id=emails(), proxy_key=keys())
    def test_add_key_for_userid_retrieve_by_userid(self, user_id, proxy_key):
        self.server.add_user_proxy_key(user_id, proxy_key)
        retrieved_key = self.server.get_user_proxy_key(user_id)
        self.assertEqual(proxy_key, retrieved_key)
        self.server.delete_user_proxy_key(user_id)


class InMemoryProxyKeyStoreTestBase(ProxyKeyStoreTestBase, unittest.TestCase):
    server = ProxyKeyStore()


class AwsProxyKeyStoreTestBase(ProxyKeyStoreTestBase, unittest.TestCase):
    server = AwsProxyKeyStore(table_name=u'proxy-key-table-nonprod')
