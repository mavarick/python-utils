#encoding:utf8
#author: mavarick


import time
import datetime
import urllib
import json
import requests
import pdb


url_api = """http://image.baidu.com/pcdutu/a_similar?queryImageUrl={queryImageUrl}&querySign={querySign}&simid={simid}&word=&querytype=0&t={t}&rn=60&sort=&fr=pc&pn=0"""
# ImageUrl
# querySign
# simid
# w
# t


# main func
def bd_shitu_api(ori_url):
    ori_url = format_url(ori_url)

    url = urllib.quote(ori_url)
    t = get_st() * 1000
    d = dict(
        queryImageUrl=url,
        t=t,
        querySign="663472127,3808469218",
        simid="20131210,1095799247219789185",
    )
    req_url = url_api.format(**d)
    print "reqeust url: ", req_url
    content = open_url(req_url)
    data = json.loads(content, encoding="utf8")
    res = ShituRes(data)
    return res


def format_url(url):
    # TODO
    return url


def open_url(url):
    resp = requests.get(url)
    code = resp.status_code
    if code != 200:
        raise Exception("url: %s, status_code: %s"%(url, code))
    return resp.content


class ShituRes(object):
    # all will expressed as UNICODE!!
    def __init__(self, data):
        self.data = data
        self.parse(data)

    def parse(self, data):
        self.total_num = data['total_num']
        self.ret_num = data['ret_num']
        self.query = data['query'].encode("utf8")
        results = []
        for item in data['result']:
            obj = ImgRes(item)
            results.append(obj)
        self.results = results

    def __str__(self):
        return "[%s::%s]" % (self.query.encode("utf8"), self.results)


class ImgRes(object):
    def __init__(self, data):
        self.data = data
        self.parse(data)

    def parse(self, data):
        self._FromPageSummary = data['FromPageSummary']
        self._ImageWidth = data['ImageWidth']
        self._ImageHeight = data["ImageHeight"]
        self._SimiValue = data['SimiValue']
        self._FromURL = data["FromURL"]
        self._ObjURL = data['ObjURL']
        self._FromURL = data['FromURL']

    def get(self, k):
        return self.data[k]

    def __getattr__(self, k):
        return self.data[k]

    def __str__(self):
        return "<%s::%s::%s::%s::%s>"%(self._FromPageSummary.encode("utf8"), self._ImageWidth,
                                       self._ImageHeight, self._ObjURL, self._SimiValue)


def get_st():
    return dt2ts(datetime.datetime.now())


def dt2ts(dt=datetime.datetime.now()):
    return time.mktime(dt.timetuple())


def str2ts(s, format="%Y-%m-%d %H:%M:%S"):
    # transform str to timestamp
    return dt2ts(datetime.datetime.strptime(s, format))


if __name__ == "__main__":
    ori_url = "http://pic.qiantucdn.com/01/24/04/00bOOOPIC66.jpg!qt780"
    bd_shitu_api(ori_url)
