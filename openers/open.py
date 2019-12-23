#!/usr/bin/env python
# encoding:utf8

import re
import traceback

from mechanize_opener import Opener as m_opener
from requests_opener import Opener as r_opener
from requests_simple_opener import Opener as rs_opener
from selenium_opener import SelOpener as s_opener

by_method={
    'm': m_opener,
    'r': r_opener,
    's': s_opener,
    'rs': rs_opener
}


def url_open(url, by='r'):
    if not url:
        raise Exception("invalid url")
    # may timeout
    try_max_time = 3
    n = 0
    opener = by_method[by]()
    while 1:
        try:
            resp = opener.open(url)
            # resp = re.sub(resp, "\xc2\xa0", "")  # replace non-breaking space
            return resp
        except:
            traceback.print_exc()
            n += 1
            if n > try_max_time:
                raise Exception("Can not open the url: [%s]"%url)
