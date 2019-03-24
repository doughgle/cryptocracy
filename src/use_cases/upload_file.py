import os

from src.boundaries.object_store import ObjectStore
from src.model.result import RESULT


class UploadFileUseCase(object):

    def __init__(self, object_store=ObjectStore()):
        self.object_store = object_store

    def run(self, request):
        """
        :type request: UploadFileRequest
        :rtype: UploadFileResponse
        """
        key = request.dest_key if request.dest_key else os.path.basename(request.source_url)
        self.object_store.put(request.source_url, key)
        url = self.object_store.get_download_url(key)
        return UploadFileResponse(result=RESULT.SUCCESS, url=url)


class UploadFileRequest(dict):
    def __init__(self, source_url, dest_key=None):
        super(UploadFileRequest, self).__init__({"source_url": source_url, "dest_key": dest_key})

    @property
    def source_url(self):
        return self.__getitem__("source_url")

    @property
    def dest_key(self):
        return self.__getitem__("dest_key")


class UploadFileResponse(dict):
    def __init__(self, result, url):
        super(UploadFileResponse, self).__init__({"result": result, "url": url})