from src.model.exceptions import InvalidInput


class ProxyKeyStore(object):

    def __init__(self):
        self.proxy_key_store = {}

    def put(self, user_id, proxy_key):
        self.proxy_key_store[user_id] = proxy_key

    def get(self, user_id):
        return self.proxy_key_store[user_id]

    def delete(self, user_id):
        del self.proxy_key_store[user_id]

    def users(self):
        return set(self.proxy_key_store.keys())

    def clear(self):
        self.proxy_key_store.clear()


import boto3
from botocore import exceptions
from boto3.dynamodb.conditions import Attr


class AwsProxyKeyStore(object):

    def __init__(self, table_name):
        if not table_name:
            raise InvalidInput("ERROR: dynamodb table is undefined.")
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(name=table_name)

    def put(self, user_id, proxy_key):
        self.table.put_item(Item={u'user_id': user_id, u'proxy_key': proxy_key})

    def get(self, user_id):
        response = self.table.get_item(Key={u'user_id': user_id})
        proxy_key = response['Item']['proxy_key']
        return proxy_key.value

    def delete(self, user_id):
        try:
            self.table.delete_item(Key={u'user_id': user_id},
                                   ConditionExpression=Attr('user_id').eq(user_id))
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise KeyError(e)

    def users(self):
        response = self.table.scan()
        return {user['user_id'] for user in response['Items']}
