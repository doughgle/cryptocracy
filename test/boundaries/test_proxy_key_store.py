import unittest

import boto3
import pytest
from hypothesis import given, settings
from hypothesis.strategies import emails, lists

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

    @settings(max_examples=1)
    @given(user_ids=lists(emails(), max_size=1))
    def test_query_users_returns_sorted_list_of_all_users_that_were_added(self, user_ids):
        self.proxy_key_store.clear()
        [self.proxy_key_store.put(user_id, keys().example()) for user_id in user_ids]
        users = self.proxy_key_store.users()
        self.assertEqual(set(user_ids), users)


@pytest.mark.skip("takes too long, produces flaky results and sends hypothesis into a crazy loop")
class AwsProxyKeyStoreTestBase(InMemoryProxyKeyStoreTestBase):

    def __init__(self, methodName):
        proxy_key_store = ClearableAwsProxyKeyStore()
        InMemoryProxyKeyStoreTestBase.__init__(self, methodName, proxy_key_store)


class ClearableAwsProxyKeyStore(AwsProxyKeyStore):

    def __init__(self):
        self.table_name = u'proxy-key-table-nonprod'
        super(ClearableAwsProxyKeyStore, self).__init__(
            table_name=self.table_name
        )

    def clear(self):
        self.table.delete()
        self.table.wait_until_not_exists()
        print('re-creating table')
        self._create_table()

    def _create_table(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            },
            SSESpecification={
                'Enabled': True,
            }
        )
        self.table.wait_until_exists()
