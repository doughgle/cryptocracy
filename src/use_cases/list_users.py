from src.model.result import RESULT


class ListUsersRequest(object):
    pass


class ListUsersResponse(dict):

    def __init__(self, users):
        super(ListUsersResponse, self).__init__({"result": RESULT.SUCCESS, "users": users})


class ListUsersUseCase(object):

    def __init__(self, proxy_key_store):
        self.proxy_key_store = proxy_key_store

    def run(self, request):
        """
        :type request: ListUsersRequest
        """
        users = self.proxy_key_store.users()
        return ListUsersResponse(users)