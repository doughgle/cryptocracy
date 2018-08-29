import unittest
from hypothesis import given
from hypothesis.strategies import text, uuids

from src.model.cloud_server import CloudServer


class TestCloudServer(unittest.TestCase):

    @given(user_id=text(), proxy_key=uuids())
    def test_add_key_for_userid_retrieve_by_userid(self, user_id, proxy_key):
        server = CloudServer()
        server.add_user_proxy_key(user_id, proxy_key)
        retrieved_key = server.get_user_proxy_key(user_id)
        self.assertEqual(proxy_key, retrieved_key)