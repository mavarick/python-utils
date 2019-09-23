#encoding:utf8
#author: mavarick


import w3lib.url


# get base url
def get_base_url(url):
    item = w3lib.url.parse_url(url)
    scheme = item.scheme.strip()
    if not scheme:
        scheme = "http"
    return "{0}://{1}".format(scheme, item.netloc)


def html_to_encode(page, encoding="utf8"):
    return w3lib.encoding.html_to_encode(None, page, default_encoding=encoding)

