import urllib.parse


class Request(object):

    def __init__(self, url: str, method: str, headers: dict):
        self.url = url
        self.path = urllib.parse.urlsplit(url).path
        self.method = method
        self.headers = headers
