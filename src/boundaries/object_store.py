import urllib2


class ObjectNotFound(urllib2.URLError):
    pass


class ObjectStore(object):
    def get(self, request_url):
        try:
            return urllib2.urlopen(request_url).read()
        except urllib2.URLError, e:
            raise ObjectNotFound(e)
