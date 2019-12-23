#!/usr/bin/env python
#encoding:utf8

# WILL BE OPTIMIZED, TODO

import os
import sys

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)


from .agent import agent_header
from .algos import random_select


def get_agent():
    header = {}
    for k, vs in agent_header.iteritems():
        v = random_select(vs)
        header[k] = v
    return header

def test():
    n = 10
    i = 0
    while i < n:
        print get_agent()
        i += 1

if __name__ == "__main__":
    test()
