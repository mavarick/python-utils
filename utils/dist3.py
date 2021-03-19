#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: dist2.py
Author: liuxufeng(liuxufeng@baidu.com)
Date: 2019/06/19 14:47:47
"""

import sys
from pandas import DataFrame, Series

def dist_range(ser, points):
    """ calculate count ratio for different bins
    """
    total_size = ser.size
    total_sum = ser.sum()
    data = []

    items = [0]
    items.extend(points)
    ts = zip(items[0:-1], items[1:])
    for p in ts:
        part_idx = ((ser > p[0]) & (ser <= p[1]))
        part_num = part_idx.sum()
        part_sum = ser[part_idx].sum()

        ratio_p = part_num * 1.0 / total_size
        ratio_sum = part_sum * 1.0 / total_sum
        data.append((p, part_num, part_sum, ratio_p, ratio_sum))
        print(p, part_num, total_size, part_sum, total_sum, ratio_p, ratio_sum)

    part_idx = (ser > points[-1])
    part_num = part_idx.sum()
    part_sum = ser[part_idx].sum()
    ratio_p = part_num * 1.0 / total_size
    ratio_sum = part_sum * 1.0 / total_sum
    data.append(((points[-1],), part_num, total_size, part_sum, total_sum, ratio_p, ratio_sum))
    print((points[-1],), part_num, total_size, part_sum, total_sum, ratio_p, ratio_sum)

    print()
    return data

def dist_range_cumsum(ser, points):
    """ calculate sample count cummulate ratio for different bins
    """
    total_size = ser.size
    total_sum = ser.sum()
    data = []
    for p in points:
        ser_p = (ser <= p).sum()
        part_idx = (ser <= p)
        part_num = part_idx.sum()
        part_sum = ser[part_idx].sum()
        ratio_p = ser_p * 1.0 / total_size
        ratio_sum = part_sum * 1.0 / total_sum
        data.append((p, part_num, total_size, part_sum, total_sum, ratio_p, ratio_sum))
        print(p, part_num, total_size, part_sum, total_sum, ratio_p, ratio_sum)
    print()
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
        print(p, ser_p, ratio_p)
    ser_p = ser[(ser > points[-1])].sum()
    ratio_p = ser_p * 1.0 / total_sum
    data.append(((points[-1],), ser_p, ratio_p))
    print((points[-1],), ser_p, ratio_p)

    print()
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
        print(p, ser_p, ratio_p)
    print()
    return data

