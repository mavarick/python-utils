#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: pair_tools.py
Author: liuxufeng(liuxufeng@baidu.com)
Date: 2018/04/26 15:31:36
"""

class PairTools(object):
    def __init__(self, name="pair_tools"):
        self.name = name

    @staticmethod
    def lcs(s1, s2):
        if not s1 or not s2:
            return []
        # s1, s2 = self.to_unicode(s1), self.to_unicode(s2)
        m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]
        d = [[None for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]

        for p1 in range(len(s1)):
            for p2 in range(len(s2)):
                if s1[p1] == s2[p2]: 
                    m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                    d[p1 + 1][p2 + 1] = 'ok'
                elif m[p1 + 1][p2] > m[p1][p2 + 1]: 
                    m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                    d[p1 + 1][p2 + 1] = 'left'
                else: 
                    m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
                    d[p1 + 1][p2 + 1] = 'up'
        (p1, p2) = (len(s1), len(s2))
        s = []
        while m[p1][p2]:  
            c = d[p1][p2]
            if c == 'ok':  
                s.append(s1[p1 - 1])
                p1 -= 1
                p2 -= 1
            if c == 'left': 
                p2 -= 1
            if c == 'up': 
                p1 -= 1
        s.reverse()
        # s = map(self.to_utf8, s)
        return s

    @staticmethod
    def lcs_len(s1, s2):
        s1_size, s2_size = len(s1), len(s2)
        up = [0] * (s1_size + 1)
        down = [0] * (s1_size + 1)
        for c2 in s2:
            for c1_idx, c1 in enumerate(s1):
                incr = 1 if c1 == c2 else 0
                down[c1_idx+1] = max(down[c1_idx], up[c1_idx+1]) + incr
            up = down[:]
        return down[s1_size]

    @staticmethod
    def to_unicode(s):
        if not isinstance(s, unicode):
            try:
                return s.decode("utf8")
            except:
                return s
        return s

    @staticmethod
    def to_utf8(s):
        if isinstance(s, unicode):
            try:
                return s.encode("utf8")
            except:
                return s
        return s

    @staticmethod
    def levenshtein(first, second):  
        if len(first) > len(second):  
            first, second = second, first  
        if len(first) == 0:  
            return len(second)
        if len(second) == 0:  
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [range(second_length) for x in range(first_length)]
        #print distance_matrix  
        for i in range(1,first_length):  
            for j in range(1,second_length):  
                deletion = distance_matrix[i-1][j] + 1  
                insertion = distance_matrix[i][j-1] + 1  
                substitution = distance_matrix[i-1][j-1]  
                if first[i-1] != second[j-1]:  
                    substitution += 1  
                distance_matrix[i][j] = min(insertion,deletion,substitution)  

        return distance_matrix[first_length-1][second_length-1]  


def test():
    # pt = PairTools()
    s1, s2 = "世界很大", "世界很好"
    s1, s2 = "世界很大", "我的宇宙"
    # s1 = s1.decode("utf8")
    # s2 = s2.decode("utf8")
    print s1, s2
    print PairTools.lcs_len(s1, s2)
    print PairTools.lcs(s1, s2)
    print PairTools.levenshtein(s1, s2)


if __name__ == "__main__":
    test()




