#encoding:utf8

''' request usage
refer to: http://my.oschina.net/dfsj66011/blog/598381
'''

import os
import sys
if __name__ == "__main__":
    sys.path.append("../")

import pdb
import requests
import cookielib
import urllib
import urlparse
import logging
from get_agent import get_agent


class Opener(object):
    def __init__(self, debug=True, timeout=10):
        self.br = None
        self.debug = debug
        self.header = None
        self.timeout=timeout

        self.initialize()

    def initialize(self):
        #self.session = requests.Session()
        self.header = get_agent()

    def open(self, url):
        #req = requests.Request('GET', url, headers=self.header)
        #prepped = self.session.prepare_request(req)
        #r = self.session.send(prepped, timeout=self.timeout)
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
             raise Exception, "NO RESPONSE data. URL:[{0}]".format(url)
        return r.text

    def reset_header(self, header_dict):
        self.header = get_agent()

    def update_header(self, header_dict):
        self.header.update(get_agent())

    def login(self, *args, **kargs):
        raise NotImplementedError('must be overwritten')

    def set_params(self, **kargs):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


# linkedin不识别utf8格式，因此只能用转义来解决这个问题
# urlparse得到的结果是unicode，在 urlunparse的时候需要转成utf8
def quote_url(url):
    url_parse = urlparse.urlparse(url)
    (scheme, netloc, path, params, query, fragment) = map(tran2utf8, (url_parse.scheme, url_parse.netloc,
        url_parse.path, url_parse.params, url_parse.query, url_parse.fragment))
    quote_path = urllib.quote(urlparse.urlunparse(("", netloc, path, params, query, fragment)))
    return "%s:%s"%(scheme, quote_path)

def tran2utf8(str):
    if isinstance(str, unicode):
        return str.encode("utf8")
    return str

def test():
    opener = Opener()
    url = "https://www.linkedin.com/topic/%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1"
    url = "https://www.linkedin.com/topic/程序设计"
    url = "https://www.baidu.com/"
    content = opener.open(url)
    print content[0:1000]

if __name__ == "__main__":
    test()

