class CloudServer(object):

    def __init__(self):
        self.proxy_key_store = {}

    def add_user_proxy_key(self, user_id, proxy_key):
        self.proxy_key_store[user_id] = proxy_key

    def get_user_proxy_key(self, user_id):
        return self.proxy_key_store[user_id]