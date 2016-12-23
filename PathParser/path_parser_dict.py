#encoding:utf8

"""
analyse path defination

输入json格式的format, 然后解析

path_parser 的阉割版,去除的功能:
    1, 全局tokens(默认的tokens);
    2, 多路径解析功能(只支持一个路径解析);
    3, 去除路径score和name值;
    4, 输出dict,

增加的功能:
    1, 分组功能

update: 20161223
  去除了多匹配的情况
  原因: 多匹配功能和unknown的自动解析功能会出现逻辑上的冲突, 多匹配理论上可以支持多路径,
    但维度上升高造成逻辑上的复杂,而且功能性并不高
"""

import re
import copy
import json
from collections import OrderedDict
import pdb


debug = False
# debug = True


class PathParser(object):
    def __init__(self, raw, multi_match_flag=0):
        self.raw = raw
        self._global_tokens = {}
        self.multi_match_flag = multi_match_flag  # 是否多field匹配
        assert self.multi_match_flag==0, "only support single match!"
        self.path_parser = self.parse_path(raw)

    def parse_path(self, s):
        parser = json.loads(s)

        tokens = parser["tokens"]
        global_tokens, global_tokens_group_num = self._parse_token(tokens)

        path_rule = parser['rule']
        path_tokens, path_tokens_dict = self._parse_path_rule(path_rule)
        path_tokens_regex = copy.deepcopy(global_tokens)
        # path_tokens_regex.update(path.get('tokens', {}))  # 去除全局tokens
        for name in path_tokens_dict:
            token_regex = path_tokens_dict[name][0]
            if token_regex not in path_tokens_regex:
                raise Exception("no defination of token name:[{0}]".format(
                    token_regex))

        path_parser = (path_rule, path_tokens, path_tokens_dict, path_tokens_regex, global_tokens_group_num)
        self._global_tokens = global_tokens
        return path_parser

    def _parse_path_rule(self, rule):
        ps = re.finditer("\[(.*?)\]", rule)
        tokens = []
        tokens_dict = OrderedDict()
        index = 1  # index 从1开始

        unknown_index = 1
        for p in ps:
            pattern = p.groups()[0]
            regex_name, score, name = pattern.split(":")
            score = float(score)
            regex_name, name = regex_name.strip(), name.strip()
            if not name:
                name = regex_name
            if name == "unknown":
                name = "{}_{}".format(name, unknown_index)
            unknown_index += 1
            tokens.append((regex_name, score, name, index))
            tokens_dict[name] = (regex_name, score, name, index)
            index += 1

        return tokens, tokens_dict

    def _parse_token(self, tokens):
        # 对于不同的字符编码
        global_tokens = OrderedDict()
        global_tokens_group_num = OrderedDict()
        if not tokens: return global_tokens
        for key in tokens:
            _regex = tokens[key]
            #
            regex, group_num = None, None
            if isinstance(_regex, list):
                # 这个时候可能存在分组的情况
                regex, group_num = _regex[0], _regex[1]
            else:
                regex = _regex
            global_tokens[key] = regex
            global_tokens_group_num[key] = group_num
        return global_tokens, global_tokens_group_num

    def parse(self, s):
        """
        parse string use parsers

        MAIN PARSER DOOR
        """
        s = to_unicode(s)
        # filter
        filter_re = getattr(self._global_tokens, 'filter', "")
        replace_re = getattr(self._global_tokens, "replace", "")
        if filter_re:
            s = re.sub(filter_re, replace_re, s)

        # delimiter
        delimiter = self._global_tokens.get("delimiter", ',')
        if delimiter is not None:  # 说明不分组. 如果不写则为None, 但是如果写了但是没值, 则为空字符串
            s_split = re.split(delimiter, s)
        else:
            s_split = [s]

        s_split = filter(lambda x:x.strip(), s_split)
        if debug: print s_split
        fields = [Field(text=s_sub) for s_sub in s_split]

        # parse
        result = self._parse(fields, self.path_parser)
        # pdb.set_trace()
        out = self.format_output(result)
        return out

    def format_output(self, result):
        d = {}
        for f in result:
            f_name = f.name
            f_text = f.text
            d.setdefault(f_name, [])
            d[f_name].append(f_text)
        data = {}
        for k, v in d.iteritems():
            data[to_utf8(k)] = "#".join(map(to_utf8, v))
        return data

    def _parse(self, fields, parser):
        (path_rule, path_tokens, path_tokens_dict, path_tokens_regex, global_tokens_group_num) = parser
        # print(u"path_name: {0}, path_score: {1}".format(path_name, path_score))
        token_levels = {}
        for token in path_tokens:
            score = token[1]
            token_levels.setdefault(score, [])
            token_levels[score].append(token)
        token_level_score_list = sorted(token_levels.iteritems(), key=lambda x:x[0], reverse=True)

        new_fields = copy.deepcopy(fields)
        if debug:
            num = 0
            print new_fields
        for score, tokens in token_level_score_list:        # score从大到小的顺序
            if debug:
                print ">>> ", num, score
                for token in tokens: print " ", token
                num += 1
                subnum = 0

            for token in tokens:                            # 从前往后的 顺序
                (regex_name, score, name, index) = token
                regex = path_tokens_regex[regex_name]
                group_num = global_tokens_group_num[regex_name]
                # 找到解析和替换的位置, 如果采用delimiter的话, 这个区间里面可能有多个值
                # 根据 待解析的field 的index,找出相应的解析index区间
                new_field_indexes = [t.index for t in new_fields]
                field_indexes = find_field_indexes(new_field_indexes, index)
                if not field_indexes:
                    continue

                if debug:
                    print "  ", subnum, token
                    for f in new_fields: print "    ", f
                    subnum += 1
                _local_fields = []
                for _index in field_indexes:
                    _local_fields.append(new_fields[_index])

                if self.multi_match_flag:
                    local_fields = self.multi_match_fields(_local_fields, regex, token, group_num)
                else:
                    local_fields = self.single_match_fields(_local_fields, regex, token, group_num)
                s, e = field_indexes[0], field_indexes[-1] + 1
                new_fields[s:e] = local_fields
        return new_fields

    def multi_match_fields(self, local_fields, regex, token, group_num):
        # 多field的匹配
        new_local_fields = copy.deepcopy(local_fields)
        while 1:
            new_local_fields_ = []
            parse_flag = 0
            for local_field in new_local_fields:
                # TAG_FIND_ONE = 1, TODO
                if local_field.index != 0:
                    new_local_fields_.append(local_field)
                    continue
                local_s = local_field.text
                r = re.search(regex, local_s)
                if r:
                    parse_flag = 1
                    start, end = r.start(), r.end()
                    value = None
                    if group_num is not None:
                        value = r.groups()[group_num]
                    _new_local_fields = self.build_new_fields(local_s, start, end, regex, token, value)
                    new_local_fields_.extend(_new_local_fields)
                else:
                    new_local_fields_.append(local_field)

            new_local_fields = new_local_fields_
            if not parse_flag:  # 如果有解析, 那么继续,如果没有的话,那么跳出
                break
        return new_local_fields

    def single_match_fields(self, local_fields, regex, token, group_num):
        # 多field的匹配
        new_local_fields = []
        for i, local_field in enumerate(local_fields):
            local_s = local_field.text
            r = re.search(regex, local_s)
            if r:
                start, end = r.start(), r.end()
                value = None
                if group_num is not None:
                    value = r.groups()[group_num]
                _new_local_fields = self.build_new_fields(local_s, start, end, regex, token, value)
                new_local_fields.extend(_new_local_fields)

                # extend 剩余的部分
                new_local_fields.extend(local_fields[(i+1):])
                return new_local_fields
            else:
                new_local_fields.append(local_field)
        return new_local_fields

    def build_new_fields(self, s, start, end, regex, token, value):
        # 当解析出来新的token的时候, 进行这种处理
        prefix, content, postfix = s[0:start], s[start:end], s[end:]
        prefix, content, postfix = prefix.strip(), content.strip(), postfix.strip()
        fields = []
        if prefix:
            fields.append(Field(text=prefix))
        if content:
            if not value:
                value = content
            fields.append(Field.from_token(token, regex, value, content))
        if postfix:
            fields.append(Field(text=postfix))
        return fields


def find_field_indexes(field_indexes, index):
    # 根据index, 找出两个解析的field之间有多个未解析的field的时候使用
    targets = []
    start = None
    end = None
    for i, f in enumerate(field_indexes):
        f_i = f
        if f_i == 0:
            if start is None:
                start = i
            else:
                end = i
        if f_i:
            if index >= f_i:
                start = None
                end = None
                continue
            else:
                end = i - 1
                break
    if end is None:  # 说明最后一个为unparsed
        end = len(field_indexes) - 1
    if start is None:
        return []
    return range(start, end + 1)


def find_field_index(fields, index):
    # 两个解析的field之间最多有1个未解析的field的时候使用
    target = None
    # index为需要解析的正则的序号
    for i, f in enumerate(fields):
        f_i = f.index
        if f_i == 0:  # 没有解析
            target = i
        if f_i:
            if index >= f.index:  # 如果相等, 那么后来的应该找之后的(因为排序就是这样)
                target = None
                continue
            else:
                return target


class Field(object):
    def __init__(self, **kwargs):
        self.regex_name = kwargs.get("regex_name", None)
        self.score = kwargs.get("score", 5)
        self.name = kwargs.get("name", "")
        self.regex = kwargs.get("regex", None)
        self.index = kwargs.get("index", 0)  # 0, 表示没有解析

        self.filled = 0
        self.text = kwargs.get("text", "")
        # 如果有值, 说明是可解析的

    def __str__(self):
        return "<{}:{}:{}:{}>".format(to_utf8(self.regex_name), to_utf8(self.name), to_utf8(self.text), self.index)

    def __unicode__(self):
        return str(self)

    @staticmethod
    def from_token(token, regex, text, raw):
        (regex_name, score, name, index) = token
        return Field(
            regex_name=regex_name,
            score=score,
            name=name,
            index=index,
            regex=regex,
            text=text,
            raw=raw,
            filled=1
        )


def to_unicode(s):
    if s is None: return u""
    if isinstance(s, str):
        return s.decode("utf8")
    return s


def to_utf8(s):
    if s is None: return ""
    if isinstance(s, unicode):
        return s.encode("utf8")
    return s

