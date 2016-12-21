#encoding:utf8
"""
  enumlate human day liveing habit and generate time interval for intellient spider
  one day has 24 hours
"""

import time
from datetime import datetime
import numpy as np
from scipy.stats import multivariate_normal


class IntervalTimeGenerator(object):
    def __init__(self, *mean_cov):
        func_list = []
        for mean, cov in mean_cov:
            f = multivariate_normal(mean=mean, cov=cov)
            func_list.append(f)
        self.func_list = func_list
        self.noice_level = 10

    def get(self, x):
        # input is one value
        # mn1= multivariate_normal(mean=10, cov=4)
        value = reduce(lambda x,y:x+y, [f.pdf([x]) for f in self.func_list]) + np.random.rand(1)/self.noice_level
        return value[0]

    def gets(self, xs):
        return [f.pdf(xs) for f in self.func_list] + np.random.rand(len(xs))/self.noice_level

    def get_by_time(self):
        _now = datetime.now()
        now = _now.hour + _now.minute * 1.0 / 60
        return self.get(now)


gen = IntervalTimeGenerator([10, 4], [15, 2], [18, 1], [21, 1])

def get_interval():
    _y = gen.get_by_time()
    y = 1.0/(_y+0.05)
    return y


