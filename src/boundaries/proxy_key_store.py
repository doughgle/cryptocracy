class ProxyKeyStore(object):

    def __init__(self):
        self.proxy_key_store = {}

    def add_user_proxy_key(self, user_id, proxy_key):
        self.proxy_key_store[user_id] = proxy_key

    def get_user_proxy_key(self, user_id):
        return self.proxy_key_store[user_id]

    def delete_user_proxy_key(self, user_id):
        del self.proxy_key_store[user_id]


import boto3


class AwsProxyKeyStore(object):

    def __init__(self, table_name):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(name=table_name)

    def add_user_proxy_key(self, user_id, proxy_key):
        self.table.put_item(Item={u'user_id': user_id, u'proxy_key': proxy_key})

    def get_user_proxy_key(self, user_id):
        response = self.table.get_item(Key={u'user_id': user_id})
        proxy_key = response['Item']['proxy_key']
        return proxy_key

    def delete_user_proxy_key(self, user_id):
        self.table.delete_item(Key={u'user_id': user_id})
