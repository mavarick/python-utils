# encoding:utf8

""" 利用腾讯文智的下载分析接口来实现 对文档的自动抽取
"""

import requests
import hmac
import hashlib
import base64
import urllib
import binascii
import json
import random


""" demo

第一步: 拿到数字签名 Signature
 {
        'Action' : 'ContentGrab',
        'Nonce' : 345122,
        'Region' : 'sz',
        'SecretId' : 'AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA',
        'Timestamp' : 1408704141,
        'url': 'http://www.qq.com'
    }

第二步: 根据数字签名和secretId查询接口
url = ("https://wenzhi.api.qcloud.com/v2/index.php?"+
       "Action=ContentGrab&Nonce=345122&Region=sz&"+
       "SecretId=AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA&Timestamp=1408704141"+
       "Signature=HgIYOPcx5lN6gz8JsCFBNAWp2oQ&url=http://www.qq.com")


"""
HOST = "wenzhi.api.qcloud.com/v2/index.php?"
url = ("https://wenzhi.api.qcloud.com/v2/index.php?"+
       "Action=ContentGrab&Nonce=345122&Region=sz&"+
       "SecretId={0}&Timestamp=1409704141"+
       "Signature={1}&url={2}")

params = {
        'Action': 'ContentGrab',
        'Nonce': 3457122,
        'Region': 'gz',
        'SecretId': 'AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA',
        'Timestamp': 1461917356,
        'url': 'http://www.qq.com'
}

SecretId = "AKIDk1ZA4Gm5gw2UncauuJrW0HLXajPzB7Na"
SecretKey = "0FGVMw5p1UDK9Pr5cAEx0f2rO6pn6mHN"

params["SecretId"] = SecretId
params['Nonce'] = random.randint(100000, 1000000)
params['url'] = "http://news.163.com/16/0429/13/BLQSSPKD0001121M.html"
params['url'] = "https://www.baidu.com/s?wd=python%20hash_hmac"  # 百度页面无法抓取
params['url'] = "http://www.linuxidc.com/Linux/2013-10/91222.htm"
params['url'] = "http://society.dbw.cn/system/2016/04/29/057198397.shtml"

# english page
params['url'] = "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html#_match_phrase_prefix" ## error
# main page
params['url'] = "http://www.163.com"  # 一群列表, not main content
params['url'] = "http://www.baidu.com/"  # still list
params['url'] = "http://www.ecocn.org/portal.php"
# params['url'] = urllib.quote("http://www.ecocn.org/portal.php?mod=view&aid=3672%20style=")  # error
params['url'] = "http://news.163.com/16/0429/08/BLQ9TRFI00014PRF.html"

# foreign page
# params['www.']


# Action = 'ContentGrab'
# Nonce = 345122
# Region = "sz"
# # SecretId
# Timestamp = "1461912358"
# url


def gen_order_param(params):
    p_list = sorted(params.items(), key=lambda x:x[0])
    p_str = '&'.join("%s=%s"%(k, v) for k, v in p_list)
    return p_str
    # return "GET"+HOST+p_str


def get_signature(url):
    # &Signature=0FGVMw5p1UDK9Pr5cAEx0f2rO6pn6mHN
    # req_url = "wenzhi.api.qcloud.com/v2/index.php?Action=ContentGrab&Nonce=345122&Region=sz&SecretId=AKIDk1ZA4Gm5gw2UncauuJrW0HLXajPzB7Na&Timestamp=1461912358&url={0}".format(url)
    req_url = "GET"+HOST+gen_order_param(params)
    print req_url
    # req_url = "GETcvm.api.qcloud.com/v2/index.php?Action=DescribeInstances&Nonce=345122&Region=gz&SecretId=AKIDz8krbsJ5yKBZQpn74WFkmLPx3gnPhESA&Timestamp=1408704141"
    # SecretKey = "Gu5t9xGARNpq86cd98joQYCN3Cozk1qA"
    signature = hmac.new(SecretKey, req_url, hashlib.sha1).digest().encode('base64').rstrip()
    print signature

    # encrype(req_url)
    signature = urllib.quote(signature)
    # sig_url = "https://wenzhi.api.qcloud.com/v2/index.php?Action=ContentGrab&Nonce=345122&Region=sz&SecretId=AKIDk1ZA4Gm5gw2UncauuJrW0HLXajPzB7Na&Timestamp=1461912358&Signature={0}&url={1}".format(signature, url)
    # print sig_url
    params['Signature'] = signature
    get_url = "https://"+HOST+gen_order_param(params)
    # resp = requests.post("https://wenzhi.api.qcloud.com/v2/index.php", data=params)
    print get_url
    resp = requests.get(get_url)
    data = resp.content
    print data
    return json.loads(data)


# def encrype(orignal):
#     hashed = hmac.new(SecretKey, orignal, hashlib.sha1)
#     baseStr = hashed.hexdigest()
#     print baseStr
#     baseStr = binascii.unhexlify(baseStr) + orignal
#     print baseStr
#     Authorization = base64.b64encode(baseStr).rstrip()
#     print Authorization



def main():
    url = "http://www.qq.com"
    data = get_signature(url)
    for k,v in data.iteritems():
        print k, v


if __name__ == "__main__":
    main()









