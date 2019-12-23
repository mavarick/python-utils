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



ZH_PUNCT = (
        # Fullwidth ASCII variants
        u'\uFF02\uFF03\uFF04\uFF05\uFF06\uFF07\uFF08\uFF09\uFF0A\uFF0B\uFF0C\uFF0D'
        u'\uFF0F\uFF1A\uFF1B\uFF1C\uFF1D\uFF1E\uFF20\uFF3B\uFF3C\uFF3D\uFF3E\uFF3F'
        u'\uFF40\uFF5B\uFF5C\uFF5D\uFF5E\uFF5F\uFF60'
        # Halfwidth CJK punctuation
        u'\uFF62\uFF63\uFF64'
        # CJK symbols and punctuation
        u'\u3000\u3001\u3003'
        # CJK angle and corner brackets
        u'\u3008\u3009\u300A\u300B\u300C\u300D\u300E\u300F\u3010\u3011'
        # CJK brackets and symbols/punctuation
        u'\u3014\u3015\u3016\u3017\u3018\u3019\u301A\u301B\u301C\u301D\u301E\u301F'
        # Other CJK symbols
        u'\u3030'
        # Special CJK indicators
        u'\u303E\u303F'
        # Dashes
        u'\u2013\u2014'
        # Quotation marks and apostrophe
        u'\u2018\u2019\u201B\u201C\u201D\u201E\u201F'
        # General punctuation
        u'\u2026\u2027'
        # Overscores and underscores
        u'\uFE4F'
        # Small form variants
        u'\uFE51\uFE54'
        # Latin punctuation
        u'\u00B7'
        u'\uFF01'  # Fullwidth exclamation mark
        u'\uFF1F'  # Fullwidth question mark
        u'\uFF61'  # Halfwidth ideographic full stop
        u'\u3002'  # Ideographic full stop
        u'\xb7'    # char ·
        )

import string
PUNCT_SET = set(ZH_PUNCT + string.punctuation + string.whitespace)


def contain_chinese(text):
    """判断字符串是否包含汉字"""
    if not text:
        return False

    try:
        u_text = text.decode("gb18030", "ignore")

        for uchar in u_text:
            if is_chinese(uchar):
                return True

    except Exception as error:
        print >> sys.stderr, "contain_chinese exception:", error
        return False

    return False


def is_punctuation(u_char):
    """判断输入字符是否为中文或英文标点

    Input:
        u_char   unicode编码字符

    Output:
        True  是标点;
        False  不是标点;
    """
    try:
        global PUNCT_SET
        if u_char in PUNCT_SET:
            return True

        return False

    except Exception as error:
        print >> sys.stderr, "is_punctuation exception:", error
        return False


def remove_punctuation(line, encoding='gbk'):
    """去除字符串中的标点符号

    Input:
        line  待去除控制字符的字符串
        encoding   待处理字符串line的编码

    Output:
        去除标点后的字符串
    """
    if not line:
        return ""

    format_line = ''
    try:
        u_line = line.decode(encoding, "ignore")
        for char in u_line:
            if is_punctuation(char):
                continue

            format_line += char

        format_line = format_line.encode(encoding, "ignore")

    except Exception as error:
        print >> sys.stderr, "remove_punctuation exception:", error
        return ''

    return format_line


