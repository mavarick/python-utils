#!/usr/bin/env python
#encoding:utf8

def is_chinese(uchar):
    '''判断unicode是否是汉字'''
    if (u'\u4e00' <= uchar <= u'\u9fa5'):
        return True
    else:
        return False


def is_number(uchar):
    '''判断是否是数字'''
    if (u'\u0030' <= uchar <= u'\u0039'):
        return True
    else:
        return False


def is_alphabet(uchar):
    '''判断是否是应为字符'''
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False

symbols_english = u',.;:?()[]{}\'"-!'
symbols_chinese = u'，。、：；“”？！——（）《》'
def is_symbol(uchar):
    '''判断是否是标点符号'''
    return (uchar in symbols_english) or (uchar in symbols_chinese)


def B2Q(uchar):
    '''半角转全角'''
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e: # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020: # 除了空格之外其他的全角半角公式为：半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return unichr(inside_code)


def Q2B(uchar):
    '''全角转半角'''
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return uchar
    else:
        return unichr(inside_code)





