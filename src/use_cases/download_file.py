from src.boundaries.object_cache import ObjectCache
from src.boundaries.object_store import ObjectStore, ObjectNotFound
from src.model.crypto import proxy_decrypt
from src.model.result import RESULT


class DownloadFileUseCase(object):
    def __init__(self, proxy_key_store):
        self.proxy_key_store = proxy_key_store
        self.object_cache = ObjectCache()
        self.object_store = ObjectStore()

    def run(self, request):
        """
        :type request: DownloadFileRequest
        """
        try:
            proxy_key = self.proxy_key_store.get(request.user_id)
            ciphertext = self.object_store.get(request.request_url)
            partially_decrypted_value = proxy_decrypt(proxy_key, ciphertext)
            expiring_object_key = request.user_id + request.request_url
            self.object_cache.put(expiring_object_key, partially_decrypted_value)
            download_url = self.object_cache.get(expiring_object_key)
            response = DownloadFileResponse(RESULT.SUCCESS, download_url=download_url)
        except KeyError:
            response = DownloadFileResponse(RESULT.FAILURE, status="FORBIDDEN")
        except ObjectNotFound:
            response = DownloadFileResponse(RESULT.FAILURE, status="NOT FOUND")
        return response


class DownloadFileRequest(object):
    def __init__(self, user_id, request_url):
        self.user_id = user_id
        self.request_url = request_url


class DownloadFileResponse(object):
    def __init__(self, result, status="OK", download_url=None):
        self._result = result
        self._status = status
        self._download_url = download_url

    @property
    def download_url(self):
        """ephemeral download url with TTL."""
        return self._download_url

    @property
    def result(self):
        return self._result

    @property
    def status(self):
        return self._status