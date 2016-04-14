#!/usr/bin/env python
# encoding:utf8

import json

from pyes import *

'''
host:
port
index
doc_type
schema: {}
'''

class ESApi(object):
    def __init__(self, config):
        self.config = config
        self.host = self.config['host']
        self.port = self.config['port']
        self.index = self.config['index']
        self.doc_type = self.config['doc_type']
        # self.schema = self.config['schema']
        # self.buld_size = self.config['bulk_size']
        self.conn = None
        self.Connect()

    def Connect(self):
        self.conn = ES("%s:%s"%(self.host, self.port), timeout=10)

    def insert(self, id, data, bulk=True):
        self.conn.index(data, self.index, self.doc_type, id=id, bulk=True)

    def update(self, id, data, **kargs):
        self.conn.update(self.index, self.doc_type, id, document=data, **kargs)

    def create_index(self, index_name):
        self.conn.indices.create_index(index_name)

    def exists_index(self, index_name):
        return self.conn.indices.exists_index(index_name)

    def put_mappings(self, **kargs):
        # doc_type, mapping, indices
        self.conn.indices.put_mapping(**kargs)

    def delete_doc_type(self, index, doc_type):
        self.conn.indices.delete_mapping(index, doc_type)

    def delete_index(self, index):
        self.conn.indices.delete_index(index)

    def delete(self, index, doc_type, id, **kargs):
        self.conn.delete(index=index, doc_type=doc_type, id=id, **kargs)

    def get(self, id):
        self.conn.get(self.index, self.doc_type, id)

    def fetchall(self, index, doc_type):
        results = self.conn.search(MatchAllQuery(), indices=index, doc_types=doc_type, scan=True)
        for r in results:
            yield r

    def flush(self):
        self.conn.indices.flush()

    def truncate(self, index, doc_type):
        pass

    def is_alive(self):
        pass


''' mapping examples:
{
  u'name': {'boost': 1.0,
             'index': 'analyzed',
             'store': 'yes',
             'type': u'string',
             "indexAnalyzer":"ik",
             "searchAnalyzer":"ik",
             "term_vector" : "with_positions_offsets"},
}
'''


