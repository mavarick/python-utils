#encoding:utf8

import time
from opener_base import Opener
from selenium import webdriver

from default_settings import OPEN_RETRY_TIMES, MAX_SLEEP_TIME

if __name__ == "__main__":
    FIREFOX_PATH = "./phantomjs-2.1.1-macosx/bin/phantomjs"
    get_sleep_time = lambda x: 0
else:
    from default_settings import FIREFOX_PATH
    from tools import get_sleep_time


class SelFirefoxOpener(Opener):
    def __init__(self, timeout=60, debug=False, **kwargs):
        super(SelFirefoxOpener, self).__init__(timeout=timeout, debug=debug, **kwargs)
        self.driver = None

    def initialize(self):
        self.driver = webdriver.Firefox(executable_path=FIREFOX_PATH)
        self.driver.set_page_load_timeout(self.timeout)

    def open(self, url):
        # selenium has no arguments of 'timeout'
        resp = self.DriverGet(url)
        return self.driver.page_source

    def DriverGet(self, url):
        # 这个地方单独隔离开来，因为很多时候这个地方可能没有加载完毕，需要看下selenium是怎么处理的
        # Todo
        n = 0
        while 1:
            try:
                sleep_time = get_sleep_time(MAX_SLEEP_TIME)
                # logger.info("sleep %s seconds"%sleep_time)
                time.sleep(sleep_time)
                # logger.info("GET: %s"%url)
                self.driver.get(url)
                break
            except:
                n += 1
                # logger.warn("have tried %s times, and sleep 1 sec"%n)
                time.sleep(1)
                if n >= OPEN_RETRY_TIMES:
                    # logger.fatal("tried %s times, and exit!"%n)
                    raise
        # time.sleep(1)

    def shutdown(self):
        if self.driver:
            try:
                self.driver.stop_client()
                # self.driver.stop_client()
            except:
                pass
        self.driver = None


def test():
    opener = SelFirefoxOpener()
    url = "www.baidu.com"
    page = opener.open(url)
    print page
    raw_input()
    opener.shutdown()


if __name__ == "__main__":
    test()
