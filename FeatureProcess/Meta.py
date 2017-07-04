#!/usr/bin/env python


class Doc(object):
    def __init__(self, label):
        self.label = label
        self.features = []

    def add_feature(self, k, v=None):
        new_f = k if isinstance(k, Feature) else Feature(k, v)
        self.features.append(new_f)


class Feature(object):
    def __init__(self, k, v):
        self._k = k
        self._v = v

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, k):
        self._k = k

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v


