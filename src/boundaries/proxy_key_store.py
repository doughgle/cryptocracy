class ProxyKeyStore(object):

    def __init__(self):
        self.proxy_key_store = {}

    def put(self, user_id, proxy_key):
        self.proxy_key_store[user_id] = proxy_key

    def get(self, user_id):
        return self.proxy_key_store[user_id]

    def delete(self, user_id):
        del self.proxy_key_store[user_id]

    @property
    def public_key(self):
        return self.__class__.__name__ + "publickey=="


import boto3


class AwsProxyKeyStore(object):

    def __init__(self, table_name):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(name=table_name)

    def put(self, user_id, proxy_key):
        self.table.put_item(Item={u'user_id': user_id, u'proxy_key': proxy_key})

    def get(self, user_id):
        response = self.table.get_item(Key={u'user_id': user_id})
        proxy_key = response['Item']['proxy_key']
        return proxy_key

    def delete(self, user_id):
        self.table.delete_item(Key={u'user_id': user_id})

    @property
    def public_key(self):
        return self.__class__.__name__ + "publickey=="
