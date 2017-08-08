#!/usr/bin/env python

import pandas as pd
from sklearn.datasets import load_svmlight_file


from Meta import Doc, Feature


class Corpus(object):
    # corpus, ensamble of docs
    def __init__(self, docs):
        self.docs = docs


class FeatureProcess(object):
    def __init__(self, corp=[]):
        self.corp = corp

    def load_svm(self, filename, sep="\t"):
        # load svm file
        features = set()
        data = []

        num = 0
        for line in open(filename):
            items = line.strip().split(sep)
            label = items[0]
            doc = Doc(label)
            for item in items[1:]:
                f, v = item.split(":")
                v = float(v)
                doc.add_feature(f, v)
            self.corp.append(doc)
            num += 1

        print("load {0} docs".format(num))

    def load_matrix(self, filename, header=None, *args, **kwargs):
        # load files as pandas
        # refer : Load datasets in the svmlight / libsvm format into sparse CSR matrix
        data = load_svmlight_file(filename)
        return data


    def load_flatten(self, filename):
        # load flatten file which could be
        # user item weight

    def save_as_svm(self, output):
        # save as svm file type

    def save_as_matrix(self, output):
        # save as matrix file type

    def save_as_flatten(self, output):
        # save as flatten file type


