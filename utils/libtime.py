#encoding:utf8

# 和 time 相关的操作


import time
import datetime


def ts2time(timestamp):
    # return datetime.datetime.utcfromtimestamp(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)


def dt2ts(dt):
    return time.mktime(dt.timetuple())


def str2ts(s, format="%Y-%m-%d %H:%M:%S"):
    # transform str to timestamp
    return dt2ts(datetime.datetime.strptime(s, format))