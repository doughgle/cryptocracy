from src.boundaries.object_cache import ObjectCache
from src.boundaries.object_store import ObjectStore
from src.model.crypto import proxy_decrypt
from src.model.result import RESULT


class DownloadFileResponse(object):
    def __init__(self, download_url):
        self._result = RESULT.SUCCESS
        self._download_url = download_url

    @property
    def download_url(self):
        """ephemeral download url with TTL."""
        return self._download_url

    @property
    def result(self):
        return self._result


class DownloadFileUseCase(object):
    def __init__(self, proxy_key_store):
        self.proxy_key_store = proxy_key_store
        self.object_cache = ObjectCache()
        self.object_store = ObjectStore()

    def run(self, request):
        proxy_key = self.proxy_key_store.get(request.user_id)
        ciphertext = self.object_store.get(request.request_url)
        partially_decrypted_value = proxy_decrypt(proxy_key, ciphertext)
        expiring_object_key = request.user_id + request.request_url
        self.object_cache.put(expiring_object_key, partially_decrypted_value)
        download_url = self.object_cache.get(expiring_object_key)
        return DownloadFileResponse(download_url)


class DownloadFileRequest(object):
    def __init__(self, user_id, request_url):
        self.user_id = user_id
        self.request_url = request_url