import unittest

from src.boundaries.proxy_key_store import ProxyKeyStore
from src.model.result import RESULT
from src.use_cases.list_users import ListUsersUseCase, ListUsersRequest


class ListUsersTest(unittest.TestCase):

    def test_list_users(self):
        proxy_key_store = ProxyKeyStore()
        proxy_key_store.put("a@b.org", "abcdef==")
        proxy_key_store.put("c@b.com", "1785988e==")
        list_users = ListUsersUseCase(proxy_key_store=proxy_key_store)
        request = ListUsersRequest()
        response = list_users.run(request)
        self.assertEqual({"result": RESULT.SUCCESS, "users": set(['c@b.com', 'a@b.org'])}, response)


if __name__ == '__main__':
    unittest.main()
