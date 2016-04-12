#!/usr/bin/env python
#encoding:utf8

import requests
import json
import urllib
import copy


RETURN_DATA = {
    "code": 0,
    "msg": "",
    "data": ""
}

class TranslateAPI(object):
    BAIDU_API = "http://fanyi.baidu.com/v2transapi/?from={0}&to={1}&query={2}"

    @staticmethod
    def translate(query, f="en", t="zh"):
        '''
        :param query: text query, must be utf8
        :param f:  from, default is 'en'
        :param t:  to, default is 'zh'
        :return:   return text
        '''
        query = query.strip()
        if not query:
            raise Exception("No query data")
        query = urllib.quote(query)
        url = TranslateAPI.BAIDU_API.format(f, t, query)

        resp = requests.get(url)
        data = json.loads(resp.content)
        if "error" in data:
            code = data.get("code", -1)
            msg = data.get("msg", "")
            raise Exception("request error: code: [%s], msg: [%s]"%(code, msg))
        tran_text = data['trans_result']['data'][0]['dst']
        return tran_text

def test():
    text = "this is a new world"
    print "这是一个新的世界"
    tran = TranslateAPI.translate(text)
    print text
    print ">> [%s]"%tran
    print "ok"

if __name__ == "__main__":
    test()






