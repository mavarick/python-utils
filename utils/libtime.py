#encoding:utf8

# 和 time 相关的操作


import time
import datetime


def ts2time(timestamp):
    # return datetime.datetime.utcfromtimestamp(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)
