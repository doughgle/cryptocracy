import urllib2
import urlparse

import boto3


class ObjectNotFound(urllib2.URLError):
    pass


class ObjectStore(object):

    def __init__(self):
        self.store = {}

    def get(self, request_url):
        try:
            return self.store[request_url]
        except KeyError as e:
            raise ObjectNotFound(e)

    def get_download_url(self, key):
        return key

    def put(self, source_url, key):
        full_url = urlparse.urlparse(source_url)
        url = ("file://" + source_url) if full_url.scheme == '' else full_url.geturl()
        data = urllib2.urlopen(url).read()
        self.put_binary(key, data)

    def put_binary(self, key, data):
        self.store[key] = data

    def delete(self, key):
        pass


class AwsObjectStore(object):

    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def put(self, source_url, key):
        self.s3.upload_file(source_url, self.bucket_name, key)

    def put_binary(self, key, data):
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def get_download_url(self, key):
        return self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': key
            },
            ExpiresIn=1800
        )

    def get(self, download_url):
        try:
            return urllib2.urlopen(download_url).read()
        except urllib2.URLError as e:
            raise ObjectNotFound(e)

    def delete(self, key):
        self.s3.delete_object(Bucket=self.bucket_name, Key=key)