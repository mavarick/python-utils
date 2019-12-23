#encoding:utf8

################################################################################################
## NEED TO BE IMPLEMENTED AND INSTALLING PantomJs
################################################################################################
#!/usr/bin/env python
# encoding:utf8

import os
import sys
import time

import commands

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_path)

if __name__ == "__main__":
    PHANTOMJS_PATH = "./phantomjs-2.1.1-macosx/bin/phantomjs"
    get_sleep_time = lambda x: 0
else:
    from default_settings import PHANTOMJS_PATH
    from tools import get_sleep_time
    from get_agent import get_agent

try:
    from selenium import webdriver
    from selenium.webdriver.common import desired_capabilities
    # import selenium.webdriver.chrome.webdriver as chrome_webdriver
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["browserName"] = "firefox"
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.disk-cache"] = True
    # cap["phantomjs.page.customHeaders.Cookie"] = 'SINAGLOBAL=3955422793326.2764.1451802953297; ' #我删掉了一大部分
    cap["phantomjs.page.customHeaders.userAgent"] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13"
    cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13"
except ImportError, ex:
    print("Waining: selenium is not installed !")

from default_settings import OPEN_RETRY_TIMES, MAX_SLEEP_TIME


class SelOpener(object):
    def __init__(self, driver_name="phantomjs", debug=False, header=None, timeout=60, **kwargs):
        self.driver_name = driver_name
        self.debug = debug
        self.header = header
        self.kwargs = kwargs

        self.driver = None
        self.timeout = timeout
        # driver: firefox, chrome, phantomjs
        # self.phantomjs_path = "/Users/mavarick/softwares/phantomjs-2.1.1-macosx/bin/phantomjs"
        self.phantomjs_path = PHANTOMJS_PATH
        # self.chromedriver_path = "/root/projects/chromedriver"
        self.initialize()

    def initialize(self, login=False):
        # if self.driver_name == "firefox":
        #     self.driver = webdriver.Firefox()
        # chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # self.driver = webdriver.Chrome(executable_path=chrome_path)
        # else:
        #     raise Exception("not supported driver")
        # if login:
        #     self.login()
        #self.driver = webdriver.PhantomJS(executable_path=self.phantomjs_path,
        #    desired_capabilities=desired_capabilities.DesiredCapabilities.CHROME.copy())

        self.driver = webdriver.PhantomJS(executable_path=self.phantomjs_path, desired_capabilities=cap)
        # 隐式等待5秒，可以自己调节
        self.driver.implicitly_wait(2)
        self.driver.set_page_load_timeout(self.timeout)
        # , desired_capabilities={"javascriptEnabled": False})
        # 设置10秒脚本超时时间
        self.driver.set_script_timeout(10)

    def set_header(self, header_dict):
        raise Exception("no need to use this, except phantomjs driver")

    def login(self, *args, **kargs):
        raise NotImplementedError('must be overwritten')

    def set_params(self, **kargs):
        for k, v in kargs.iteritems():
            setattr(self, k, v)

    def reset(self):
        self.initialize()

    def open(self, url):
        # selenium has no arguments of 'timeout'
        resp = self.DriverGet(url)
        source = self.driver.page_source
        return source

    def DriverGet(self, url):
        # 这个地方单独隔离开来，因为很多时候这个地方可能没有加载完毕，需要看下selenium是怎么处理的
        # Todo
        n = 0
        while 1:
            #self.check_process()
            if not self.driver:
                self.initialize()
            try:
                sleep_time = get_sleep_time(MAX_SLEEP_TIME)
                # logger.info("sleep %s seconds"%sleep_time)
                time.sleep(sleep_time)
                # logger.info("GET: %s"%url)
                self.driver.get(url)
                break
            except:
                self.shutdown()
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

    def check_process(self):
        cmd = "ps aux | grep phantomjs | grep -v grep | wc -l"
        code, msg = commands.getstatusoutput(cmd)
        if code != 0:
            return
        try:
            phantomjs_number = int(msg)
            if phantomjs_number > 10:
                cmd = "ps aux | grep phantomjs | grep -v grep | awk '{print $2}' | xargs kill -9"
                code, msg = commands.getstatusoutput(cmd)
                if code != 0:
                    print("Error when kill phantomjs process")
        except:
            return


# # linkedin不识别utf8格式，因此只能用转义来解决这个问题
# # urlparse得到的结果是unicode，在 urlunparse的时候需要转成utf8
# def quote_url(url):
#     url_parse = urlparse.urlparse(url)
#     (scheme, netloc, path, params, query, fragment) = map(tran2utf8, (url_parse.scheme, url_parse.netloc,
#         url_parse.path, url_parse.params, url_parse.query, url_parse.fragment))
#     quote_path = urllib.quote(urlparse.urlunparse(("", netloc, path, params, query, fragment)))
#     return "%s:%s"%(scheme, quote_path)

# def tran2utf8(str):
#     if isinstance(str, unicode):
#         return str.encode("utf8")
#     return str

from bs4 import BeautifulSoup as BS

def test():
    # phantomjs_path = "/root/projects/phantomjs-debian-master/phantomjs-1.9.7-linux-x86_64/bin/phantomjs"
    # chromedriver_path = "/root/projects/chromedriver"

    capabilities = desired_capabilities.DesiredCapabilities.CHROME.copy()

    driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, desired_capabilities=capabilities)
    # driver = chrome_webdriver.WebDriver(executable_path=chromedriver_path,
    #                                     desired_capabilities=capabilities)

    url = "http://www.alexa.cn/index.php?url=baidu.com"
    driver.get(url)
    print "driver name: ", driver.name
    page = driver.page_source
    bs = BS(page)
    biaoge_divs = bs.find_all("div", "biaoge")
    print biaoge_divs[2].text


def test_2():
    import pdb
    sel_opener = SelOpener()
    url = "http://www.alexa.cn/index.php?url=baidu.com"
    page = sel_opener.open(url)

    pdb.set_trace()
    bs = BS(page)
    biaoge_divs = bs.find_all("div", "biaoge")
    print biaoge_divs[2].text

if __name__ == "__main__":
    test_2()
