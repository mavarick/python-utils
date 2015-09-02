#!/usr/bin/env python
#encoding:utf8
'''
refer: http://blog.csdn.net/mr__fang/article/details/7089581
'''
import xlrd

''' 问题：如果采用namedtuple的话，那么就会对head有要求(不能用空格等)
'''
def read_xls(filename, sheet_name="", with_head=False):
    data = xlrd.open_workbook(filename)

    if sheet_name:
        table = data.sheet_by_name(sheet_name)
    else:
        table = data.sheets()[0]

    nrows, ncols = table.nrows, table.ncols

    heads = []
    data = []

    if with_head: 
        heads = table.row_values(0)
    else: 
        heads = range(ncols)
        data.append(table.row_values(0))
    for row_index in range(1, nrows):
        data.append(table.row_values(row_index))
    return heads, data

''' read excel file with pandas
import pandas
'''
import pandas as pd

def read_xlsx_with_pandas(filename, sheet_name="", header=0, fields={}):
    if not sheet_name: sheet_name=0  # the first sheet
    data = pd.read_excel(filename, sheet_name, header=header, converters=fields)
    '''
    for k, field_parser in fields.iteritems():
        data[k] = field_parser(data[k])
    '''
    return data

def test_read_xlsx_with_pandas():
    filename = 'temp/test.xlsx'
    field_types= {
        u'月份': pd.to_datetime, #pd.DatetimeIndex,
        u'日期': pd.to_datetime, #pd.DatetimeIndex
    }
    data = read_xlsx_with_pandas(filename, fields=field_types)
    print data[u'月份']

def test():
    filename = "temp/test.xlsx"
    heads, data = read_xls(filename, with_head=True)
    print heads
    print data[0]


if __name__ == "__main__":
    #test()
    test_read_xlsx_with_pandas()



    
