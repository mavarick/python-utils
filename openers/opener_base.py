#!/usr/bin/env python
#encoding:utf8


class Opener(object):
    def __init__(self, debug=True, timeout=10, **kwargs):
        self.br = None
        self.debug = debug
        self.header = None
        self.timeout=timeout

        self.initialize()

    def initialize(self):
        # for initialize this openers
        # self.header = None
        pass

    def open(self, url):
        raise NotImplementedError

    def reset_header(self, header_dict):
        # reset the header
        pass

    def reset_cookie(self, cookie_path):
        # reset cookie: clear the old and generate the new one
        # you could also build one urlserver for specified site
        pass

    def login(self, *args, **kargs):
        raise NotImplementedError('must be overwritten')

    def set_params(self, **kargs):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

