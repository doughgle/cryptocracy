from src.boundaries.object_store import ObjectStore, ObjectNotFound
from src.model import user_id
from src.model.abe_scheme import NullCipher, DecryptionFailed
from src.model.exceptions import InvalidInput
from src.model.object_cache_lookup_key import make_lookup_key
from src.model.result import RESULT, STATUS


class DownloadFileUseCase(object):
    def __init__(self, get_cloud_server_secret_key_func, proxy_key_store, object_store=ObjectStore(), object_cache=ObjectStore(),
                 abe_scheme=NullCipher()):
        self.get_cloud_server_secret_key_func = get_cloud_server_secret_key_func
        self.proxy_key_store = proxy_key_store
        self.object_cache = object_cache
        self.object_store = object_store
        self.abe_scheme = abe_scheme

    def run(self, request):
        """
        :type request: DownloadFileRequest
        :rtype DownloadFileResponse
        """
        try:
            user_id.assert_valid(request.user_id)
            proxy_key = self.proxy_key_store.get(request.user_id)
            ciphertext = self.object_store.get(request.request_url)
            cloud_server_secret_key = self.get_cloud_server_secret_key_func()
            partially_decrypted_value = self.abe_scheme.proxy_decrypt(cloud_server_secret_key,
                                                                      proxy_key_user=proxy_key,
                                                                      ciphertext=ciphertext)
            expiring_object_key = make_lookup_key(request.request_url, request.user_id)
            self.object_cache.put_binary(expiring_object_key, partially_decrypted_value)
            download_url = self.object_cache.get_download_url(expiring_object_key)
            response = DownloadFileResponse(RESULT.SUCCESS, download_url=download_url)
        except (KeyError, DecryptionFailed):
            response = DownloadFileResponse(RESULT.FAILURE, status=STATUS.FORBIDDEN)
        except ObjectNotFound:
            response = DownloadFileResponse(RESULT.FAILURE, status=STATUS.NOT_FOUND)
        except InvalidInput as e:
            response = DownloadFileResponse(RESULT.FAILURE, status=STATUS.BAD_REQUEST, message=e.message)
        return response


class DownloadFileRequest(object):
    def __init__(self, user_id, request_url):
        self.user_id = user_id
        self.request_url = request_url


class DownloadFileResponse(dict):
    def __init__(self, result, status=STATUS.OK, download_url=None, message=None, content=None):
        super(DownloadFileResponse, self).__init__({"result": result,
                                                    "status": status,
                                                    "download_url": download_url,
                                                    "message": message,
                                                    "content": content})

    @property
    def download_url(self):
        """ephemeral download url with TTL."""
        return self.__getitem__("download_url")

    @property
    def result(self):
        return self.__getitem__("result")

    @property
    def status(self):
        return self.__getitem__("status")

    @property
    def message(self):
        return self.__getitem__("message")
