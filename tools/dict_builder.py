#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DictBuilder(object):
    def __init__(self, sep_item="#", sep_kv=":"):
        self.sep_item = sep_item
        self.sep_kv = sep_kv
        self.d = {}

    def load(self, s):
        items = filter(lambda x:x, s.split(self.sep_item))
        for item in items:
            k, v = item.split(self.sep_kv)
            self.d[k] = self.d.get(k, 0.0) + float(v)
        return self

    def load_list(self, arr, value=1):
        for k in arr:
            self.load_item(k, value)
        return self

    def load_item(self, k, value=1):
        self.d[k] = self.d.get(k, 0.0) + value
        return self

    def tostr(self, max_num=-1):
        items = sorted(self.d.iteritems(), key=lambda x:x[1], reverse=True)
        if max_num >= 0:
            items = items[0:max_num]
        return self.sep_item.join(["%s%s%s"%(k, self.sep_kv, v) for (k, v) in items])


def test():
    db = DictBuilder("#", ":")
    s = "世界:1#大大:5"
    print db.load(s).tostr()
    print db.load(s).tostr()
    arr = ["世界", "宇宙", "abdc", 123, '世界', '世界']
    print db.load_list(arr).tostr()


if __name__ == "__main__":
    test()
    



