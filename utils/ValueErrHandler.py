#!/usr/bin/env python
# encoding:utf8

''' USAGE:
1, number of default values and variables in `with sentence` must be same!
    if `__exit__` return True, and numbers are not matched, some unexpected errors could happen
2,
'''



class ValueErrHandler(object):
    def __init__(self, *default_values):
        # default_values: values
        self.default = default_values

    def __enter__(self):
        # print ">>", self.default
        return self.default

    def __exit__(self, exc_type, exc_value, exc_tb):
        # return True to ignore the errors, in exc_tb
        return True

def test_ErrorHandler_1():
    with ValueErrHandler("12345") as (num, value):
        num = 10
        value = 1/0
    print value
    print num

    print "Got here!!!!"

def test_ErrorHandler_2():
    with ValueErrHandler("12345") as (value,):
        num = 10
        value = 1/0
    print value
    print num

    print "Got here!!!!"


# test_ErrorHandler_1()
test_ErrorHandler_2()