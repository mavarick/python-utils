#!/usr/bin/env python
#encoding:utf8

import tornado.web
import tornado.ioloop
import sys
import optparse
import json
import pdb

filename = ''
port = 9000
cols = '0'  # column number
sep = '\t'
key = None
whole=0

parser = optparse.OptionParser()
parser.add_option('-f', '--file', help="json file", dest='filename', default=filename)
parser.add_option('-p', '--port', help='api port', dest='port', default=port)
parser.add_option('-c', '--cols', help='column number, start from 1', dest='cols', default=cols)
parser.add_option('-s', '--sep', help='seperator', dest='sep', default=sep)
parser.add_option('-k', '--key', help="key column number", dest='key', default=key)
parser.add_option('-w', '--whole', help="read as one whole file", dest='whole', default=whole)


'''
examples
--------
1, each line is one json structure
    python webapi.py -f file
2, specify the cols and key for each line
    python webapi.py -f file -c 5 -t '\t' -k 1

'''
(options, args) = parser.parse_args()

print(">> Start ..")
options = options.__dict__
print options
for k, v in options.iteritems():
    if k == 'filename':
        filename = v
    if k == 'port':
        port = int(v)
    if k == 'sep':
        sep = v
    if k == 'cols':
        cols = map(int, v.split(sep))
    if k == 'key':
        key = int(v) if v else None
    if k == 'whole':
        whole = int(v)
if not filename:
    print parser.print_help()
    sys.exit()

data = {}
n = 0
num_cols = 0

raw_data = []
if whole:
    raw_data.append(open(filename).read().strip().split(sep))
else:
    for line in open(filename):
        items = line.strip().split(sep)
        raw_data.append(items)

for items in raw_data:
    if n == 0:
        if key > len(items):
            print("Warn: the key value is above the number of items, so not used")
            key = None
        if not cols:
            cols = [0]
        else:
            func = lambda x: len(items) if x > len(items) else x
            cols = list(set([func(t) for t in cols]))
            cols.sort()
        num_cols = len(cols)
    if num_cols == 1:
        item_data = items[cols[0]]
    else:
        item_data = [items[t] for t in cols]
    if key:
        item_key = items[key]
    else:
        item_key = n + 1
    data[item_key] = item_data
    n += 1

data_len = len(data)
print(">> total line: {}".format(data_len))

class JsonWatcher(tornado.web.RequestHandler):
    def get(self):
        id = int(self.get_argument('id', 1))
        id = data_len if id > data_len else id
        print("> Get Id: {}".format(id))
        content = (data[id])
        #print ">>", content
        #content = content.replace(r'\"', '"')

        self.set_header("Content-Type", "application/json")
        self.write(content)

apps = [(r'/', JsonWatcher)]

print "PORT: %s"%port
application = tornado.web.Application(apps)
application.listen(port)
tornado.ioloop.IOLoop.instance().start()



