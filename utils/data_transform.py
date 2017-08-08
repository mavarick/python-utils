#!/usr/bin/env python
#encoding:utf8

'''
read input data, transform it to other types
svm format:
    label k1:v1 k2:v2 ......
matrix format:
    label header1 header2...
    0 v1 v2 ...
'''
import sys
import optparse



input_file = "input.dat"
out_file = "out.dat"
handle_type = ''
sep = '\t'
default=0.0
analysis=None

parser = optparse.OptionParser()
parser.add_option("-f", '--from', help='input file', dest='input_file', default="input.dat")
parser.add_option("-o", '--out', help='to output file', dest='out_file', default='out.dat')
parser.add_option("-t", '--type', help='handling type: svm2matrix matrix2svm', 
    dest='handle_type', default='svm2matrix')
parser.add_option("-s", '--sep', help='seperator', dest='sep', default='\t')
parser.add_option("-d", '--default', help='default value', dest='default', default=0.0)
parser.add_option("-a", '--analysis', help='analyse the data, -t should be: svm or matrix', 
    action='store_true', default=None)

(options, args) = parser.parse_args()
options = options.__dict__
print options
for k, v in options.iteritems():
    if k == 'input_file':
        input_file = v
    if k == 'out_file':
        out_file = v
    if k == 'handle_type':
        handle_type = v
    if k == 'sep':
        sep = v
    if k == 'default':
        default=v
    if k == 'analysis':
        analysis = v  # true or none

def read_svm_file(input_file, sep='\t', default=(0.0)):
    '''read svm data file, with format:
    label k1:v1 k2:v2 ....

    Parameters
    ----------
    input_file

    Returns
    -------
    features: sorted list of strings, name of features
    data: list of samples.
        sample format: (label, {k1: v1, k2: v2, ...})
    '''
    default = str(default)
    features = set()
    data = []

    samples_num = 0
    features_num = 0
    for line in open(input_file):
        items = line.strip().split(sep)
        label = items[0]
        feature_dict = {}
        for item in items[1:]:
            f, v = item.split(":")
            features.add(f)
            feature_dict[f] = v
        data.append((label, feature_dict))
    features = list(features)
    features.sort()
    print("info>> Sample Cnt [{0}]".format(len(data)))
    print("info>> Feature Cnt [{0}]".format(len(features)))
    return features, data

def dict2matrix(features, data, out_file, sep='\t', default=(0.0)):
    #features, data = read_svm_file(input_file, sep=sep, default=default)
    out = open(out_file, 'w')
    print >>out, '\t'.join(['label'] + features)
    for item in data:
        label, feature_dict = item
        new_feature_list = [label]
        for f in features:
            v = feature_dict.get(f, default)
            new_feature_list.append(str(v))
        print >>out, '\t'.join(new_feature_list)

def svm2matrix(input_file, out_file, sep='\t', default=0.0):
    features, data = read_svm_file(input_file, sep=sep, default=default)
    dict2matrix(features, data, out_file, sep=sep, default=default)

if handle_type == 'svm2matrix':
    svm2matrix(input_file, out_file, sep=sep, default=default)
    print("Done!")


