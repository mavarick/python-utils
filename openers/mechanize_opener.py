#encoding:utf8

import os
import sys
if __name__ == "__main__":
    sys.path.append("../")

import cookielib
import urllib
import urlparse
from get_agent import get_agent


try:
    import mechanize
except Exception, ex:
    print("Warn: mechanize is not installed")


class Opener(object):
    def __init__(self, debug=True):
        self.br = None
        self.debug = debug
        self.header = None

        self.initialize()

    def initialize(self):
        br = mechanize.Browser(history=NoHistory())
        # cj = cookielib.LWPCookieJar()
        cj = cookielib.MozillaCookieJar()
        br.set_cookiejar(cj)

        br.set_handle_equiv(True)
        # br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # br.set_debug_http(self.debug)
        # br.set_debug_redirects(self.debug)
        # br.set_debug_responses(self.debug)
        self.br = br

    def reset_header(self, header_dict):
        self.br.addheaders = header_dict.items()

    def update_header(self, header_dict):
        try:
            old_headers = dict(self.br.addheaders)
        except:
            old_headers = {}
        headers = old_headers
        headers.update(header_dict)
        # for k, v in headers.iteritems():
        #     print k, v
        self.br.addheaders = headers.items()

    def login(self, *args, **kargs):
        raise NotImplementedError('must be overwritten')

    def set_params(self, **kargs):
        for k, v in kargs.iteritems():
            setattr(self, k, v)

    def reset(self):
        self.initialize()

    def open(self, url, timeout=30.0, header=None):  # None, reset, update
        if header == 'reset':
            new_header = get_agent()
            self.reset_header(new_header)
        if header == "update":
            new_header = get_agent()
            self.update_header(new_header)
        # print "url>>", url
        url = quote_url(url)
        resp = self.br.open(url, timeout=timeout)
        content = resp.read()
        return content


class NoHistory(object):
    def add(self, *a, **k): pass

    def clear(self): pass


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
    opener.initialize()
    url = "https://www.linkedin.com/topic/%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1"
    url = "https://www.linkedin.com/topic/程序设计"
    content = opener.open(url)
    print content[0:1000]

if __name__ == "__main__":
    test()

