import urllib2


class ObjectStore(object):
    def get(self, request_url):
        return urllib2.urlopen(request_url).read()