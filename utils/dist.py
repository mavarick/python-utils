#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: dist.py
Author: liuxufeng(liuxufeng@baidu.com)
Date: 2018/09/07 20:48:52
"""
#!/usr/bin/env python

import sys
from pandas import DataFrame, Series

def dist_range(ser, points):
    """ calculate count ratio for different bins
    """
    total_size = ser.size
    data = []

    items = [0]
    items.extend(points)
    ts = zip(items[0:-1], items[1:])
    for p in ts:
        ser_p = ((ser > p[0]) & (ser <= p[1])).sum()
        ratio_p = ser_p * 1.0 / total_size
        data.append((p, ser_p, ratio_p))
        print >>sys.stdout, p, ser_p, ratio_p
    ser_p = (ser > points[-1]).sum()
    ratio_p = ser_p * 1.0 / total_size
    data.append(((points[-1],), ser_p, ratio_p))
    print >>sys.stdout, (points[-1],), ser_p, ratio_p

    print >>sys.stdout
    return data

def dist_range_cumsum(ser, points):
    """ calculate sample count cummulate ratio for different bins
    """
    total_size = ser.size
    data = []
    for p in points:
        ser_p = (ser <= p).sum()
        ratio_p = ser_p * 1.0 / total_size
        data.append((p, ser_p, ratio_p))
        print >>sys.stdout, p, ser_p, ratio_p
    print >>sys.stdout
    return data

def sum_dist_range(ser, points):
    total_sum = ser.sum()
    data = []

    items = [0]
    items.extend(points)
    ts = zip(items[0:-1], items[1:])
    for p in ts:
        ser_p = ser[((ser > p[0]) & (ser <= p[1]))].sum()
        ratio_p = ser_p * 1.0 / total_sum
        data.append((p, ser_p, ratio_p))
        print >>sys.stdout, p, ser_p, ratio_p
    ser_p = ser[(ser > points[-1])].sum()
    ratio_p = ser_p * 1.0 / total_sum
    data.append(((points[-1],), ser_p, ratio_p))
    print >>sys.stdout, (points[-1],), ser_p, ratio_p

    print >>sys.stdout
    return data

def sum_dist_range_cumsum(ser, points):
    """ calculate sample count cummulate ratio for different bins
    """
    total_sum = ser.sum()
    data = []
    for p in points:
        ser_p = ser[(ser <= p)].sum()
        ratio_p = ser_p * 1.0 / total_sum
        data.append((p, ser_p, ratio_p))
        print >>sys.stdout, p, ser_p, ratio_p
    print >>sys.stdout
    return data

