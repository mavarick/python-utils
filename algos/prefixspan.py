#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: prefixspan.py
Author: liuxufeng(liuxufeng@baidu.com)
Date: 2019/01/08 17:04:25
"""

import math


class PrefixSpan(object):
    def __init__(self, support=0.5, confidence=0.8):
        self.support = 0.5
        self.confidence = 0.8

    def process(self, arrs):
        pass


def prefixspan(arrs, support, confidence):
    while 1:
        freqs = find_freq(arrs, len(arrs), support)
        for freq, freq_size in freqs:
            freq_lefts = cut_freq_postfix(arrs, freq)
            valid_freq_lefts = filter(lambda x: x, freq_lefts)
            
            
    

def cut_freq_postfix(arrs, freq):
    lefts = []
    for arr in arrs:
        try:
            idx = arr.index(freq)
        except:
            idx = len(arr)
            
        left = arr[(idx+1):]
        lefts.append(left)
    return lefts


def find_freq(arrs, size, support=0.5):
    """ calculate char support
    @arrs
    @size, denominator of support
    @support, minimum of support
    """
    sup_map = {}
    for arr in arrs:
        char_set = set(arr)
        for c in char_set:
            sup_map.setdefault(c, 0)
            sup_map[c] += 1
    min_sup_size = int(math.ceil(size * support))
    sup_list = [(k, v) for (k, v) in sup_map.iteritems() if v >= min_sup_size]
    sup_list.sort(key=lambda x:x[1], reverse=True)
    return sup_list
    
            
            




