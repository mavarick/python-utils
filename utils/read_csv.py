#!/usr/bin/env python
#encoding:utf8

''' read csv file

use `enca` to detect file coding
use `icova` to transform file coding
'''
import csv
import pdb

def read_csv(filename, with_head=False, decode_char="gb2312", delimiter=';'):
    reader = csv.reader(open(filename, 'rU'), dialect=csv.excel_tab, delimiter=delimiter)
    data = []
    for item in reader:
        data.append([t.decode(decode_char) for t in item])
    if not data:
        return [], []
    if with_head:
        head, data = data[0], data[1:]
    else:
        head, data = range(len(data[0])), data
    return head, data

def read_csv_2(filename, with_head=False, decode_char="gb2312"):
    with open(filename, 'r') as f:
        reader = csv.reader(f.read().splitlines())
        data = [row for row in reader]
    return data

def read_csv_3(filename, *args, **kargs):
    ''' use numpy.genfromtxt function to read csv file
    '''
    import numpy as np
    data = np.genfromtxt(filename, names=True, delimiter=';', dtype=())
    pdb.set_trace()

def read_csv_with_pandas(filename, header=0, decode="utf8", sep=';'):
    pass



def test():
    filename = "temp/test2.csv"
    '''
    head, data = read_csv(filename, with_head=True)
    print head
    print data[:2]
    '''
    read_csv_3(filename)


if __name__ == "__main__":
    test()
'''
refer:http://stackoverflow.com/questions/17315635/csv-new-line-character-seen-in-unquoted-field-error

error message: 
    new-line character seen in unquoted field - do you need to open the file in universal-newline mode


It'll be good to see the csv file itself, but this might work for you, give it a try, replace:

file_read = csv.reader(self.file)

with:

file_read = csv.reader(self.file, dialect=csv.excel_tab)

Or, open a file with universal newline mode and pass it to csv.reader, like:

reader = csv.reader(open(self.file, 'rU'), dialect=csv.excel_tab)

Or, use splitlines(), like this:

def read_file(self):
    with open(self.file, 'r') as f:
        data = [row for row in csv.reader(f.read().splitlines())]

'''

'''
有关编码问题：
csv读出来的数据很多时候是乱码： http://blog.csdn.net/wujingwen1111/article/details/7802723
说的不一定正确，但是还是可取的

1）当读入的文件出现“\xef\xbb\xbf”时，可以通过“utf-8-sig”解码修正。如：

[python] view plaincopy

    line = f.readline()  
    line = line.decode('utf-8-sig')  


2）当读入的文件出现“\ufeff”时，可以通过“utf-8”解码修正。如：

[python] view plaincopy

    line = f.readline()  
    line = line.decode('utf-8')  


3）当读入的中文出现乱码，如“\u4e2d\u56fd\u79fb\u52a817”的时候，可以通过“gb2312”解码修正。如：

[python] view plaincopy

    line = f.readline()  
    line = line.decode('gb2312')  


'''