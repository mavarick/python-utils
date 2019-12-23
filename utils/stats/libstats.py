#encoding:utf8
#author: mavarick


"""
mainly tools to do array analysis
"""


import pandas as pd
import numpy as np


class ArrayTools(object):
    @classmethod
    def describe(cls, array):
        ser = pd.Series(array, dtype=np.float32)
        skew = ser.skew()
        cov = ser.cov(ser)
        ret = dict(
            min=ser.min(),
            max=ser.max(),
            mean=ser.mean(),
            count=ser.count(),
            sum=ser.sum(),
            cov=0 if np.isnan(cov) else cov,
            skew=0 if np.isnan(skew) else skew,
        )
        return ret
