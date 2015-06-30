#!/usr/bin/env python
#encoding:utf8

# io.py

import pdb
import sys
import traceback
import pandas as pd
import numpy as np

def parse_dtypes(dtypes):
    ''' parse the dtyps list, generate different parts of arguments for pandas read_csv/table functions
    '''
    dtype = {}
    parse_dates = []
    default_value_dict = {}
    converters = {}
    field_names = []
    num = 0
    for index in range(len(dtypes)):
        index_or_name, _t, _func, default_value = dtypes[index]
        field_names.append(index_or_name)
        # handle default values, when the value is NaN, then fillit
        if default_value is not None:
            default_value_dict[index_or_name] = default_value
        # converters
        if _func.__name__ not in np.__dict__:
            converters[index_or_name] = _func
            continue
        # parse_dates
        if _t in [np.datetime64]:
            parse_dates.append(index_or_name)
            continue
        # dtype
        dtype[index_or_name] = _t
    return dtype, parse_dates, converters, default_value_dict, field_names


DEFAULT_TYPE=unicode
DEFAULT_PARSER=unicode
DEFAULT_VALUE=None
TYPE_DEFAULT_VALUE={
    unicode: '',
    # others: None
}
TYPE_DEAFULT_PARSER={
    unicode:unicode,
}
def parse_field_format(field_item):
    '''parse input field

    just for convinience

    Parameters
    ----------
    field_item: tuple with length 1/2/3/4
        field_item is of type tuple:
        complete format is (field_name, type, parser, default), for convinience, defile:
        :(name, ) : with type/parser are all np.unicode, and default_val is None
        :(name, type, ): with parse_func = type, and default is None
        :(name, type, parser, ): with default is None
        or of type dict:
        {"name": name, 'type'=type, 'parser': parser, 'default':default_val}
        :{"name": name}: type/parser='unicode', default is None
        :{"name": name, "default":default}: type/parser = unicode
        :{"name": name, "type": type, "default":default}: parser=type

    Returns
    -------
    (name, type, parser, default)
        the complete format

    Notes
    -----
    1, default value of unicode type is ''
    '''
    if type(field_item) in [dict]:
        name = field_item.get('name')
        field_type = field_item.get('type', unicode)
        field_parser = field_item.get("parser", unicode)
        default = field_item.get("default", TYPE_DEFAULT_VALUE.get(field_type, None))
    elif type(field_item) in [list, tuple]:
        args_number = len(field_item)
        if args_number == 1:
            name = field_item[0]
            field_type = DEFAULT_TYPE
            field_parser = TYPE_DEAFULT_PARSER.get(field_type, DEFAULT_PARSER)
            default = TYPE_DEFAULT_VALUE.get(field_type, DEFAULT_VALUE)
        elif args_number == 2:
            name, field_type = field_item
            field_parser = TYPE_DEAFULT_PARSER.get(field_type, DEFAULT_PARSER)
            default = TYPE_DEFAULT_VALUE.get(field_type, DEFAULT_VALUE)
        elif args_number == 3:
            name, field_type, field_parser = field_item
            default = TYPE_DEFAULT_VALUE.get(field_type, DEFAULT_VALUE)
        elif args_number == 4:
            name, field_type, field_parser, default = field_item
            if field_parser == None: field_parser = field_type
        else:
            raise (Exception, "Error: Arguments Number is out of [1, 2, 3 4]")
    else:
        raise (Exception, "Error: Field Type must be dict/list/tuple")
    return (name, field_type, field_parser, default)

def parse_field_format_from_dict(dtypes):
    '''parse field type from dict,

    more easier way to use read_csv, especially with very many columns

    Parameters
    ----------
    dtypes: dict, with format: 
        {
        (np.float32, default_val): ['col1', 'col2', ...],
        (np.float32, default_val2): ['col11', 'col22', ...]
        (np.datetime64, default_val3): ['col3', 'col4', ...]
        }

    Returns
    -------
    [(name, type, parser, default)]
    '''
    parsed_dtypes = []
    for (_t, default_val), fields in dtypes.iteritems():
        for field in fields:
            parsed_dtypes.append(parse_field_format(
                    {'name': field, 'type': _t, 'default': default_val}
                ))
    return parsed_dtypes

def parse_field_format_from_list(dtypes):
    '''parse defined field format

    Parameters
    ----------
    dtypes: list of tuple or dict,
        tuple: (name, type, parser, default)
        dict:  {"name": name, 'type'=type, 'parser': parser, 'default':default_val}
    '''
    return [parse_field_format(field) for field in dtypes]

def parse_fields(dtypes):
    return {
        dict: parse_field_format_from_dict, 
        list:parse_field_format_from_list
        }[type(dtypes)](dtypes)

def read_csv(filename, dtypes=[], sep=';', error_bad_lines=True, filter_names=True, 
        header=0, encoding='utf8', force_datetime_transform=True, fillna=True, **kargs):
    '''read csv just for detecting data errors

    first load the data with unicode to memory, then use array-level method to transform it
    if data errors happened, program will show out relevent info.
    then na_values could be used to let these wrong values to be NaN.

    Parameters
    ----------
    filename: string
    dtypes: list, dict
        define the relavant information of column 
    force_datetime_transform: bool
        used as `coerce` argument in pd.to_datetime()
    filter_names: bool
        indicate weather to just load columns define in types or not
    fillna: bool, default is True
        fill colomn with specified default value in dtypes
        if error happens, columns will not fill NaN.
    other parameters: plz see pandas.read_csv

    Returns
    -------
    data: pandas.DataFrame

    Examples
    --------
    # for data:
    id;name;amount;number;dtime
    1;雨伞;10.5;5;2011/1/1 6:05
    2;帽子;;;2012/2/3 1:20
    3;书籍;aaa;20;2012/3/11 1:20
    4;背包;30;a;2012/3/11 1:20
    5;HUADUO;30;70.9;Jan 1, 2014
    6;台灯;100;20;0

    # define relavant variables
    filename = 'mock.csv'
    # defile dtypes
    dtypes = [
        # (field_name/field_index, type, func, default_value) 
        ('id', np.int32, None,  ''),
        ('name', unicode, None, ''),  
        ('amount', np.float32, None, 0.0),
        ('number', np.int32, None, 0.0),
        ('dtime', np.datetime64, None, None)
    ]
    data = read_csv(filename, dtypes=dtypes, sep=';')
    # could see error information on console
    > check [amount]..
        [Warn] use element-level transform ..
            *Error: Index[2], Item[aaa], To Type[<type 'numpy.float32'>]
    > check [number]..
         [Warn] use element-level transform ..
            *Error: Index[1], Item[nan], To Type[<type 'numpy.int32'>]
            *Error: Index[3], Item[a], To Type[<type 'numpy.int32'>]
            *Error: Index[4], Item[70.9], To Type[<type 'numpy.int32'>]

    Notes
    -----
    field type limited to:
        unicode, str
        np.datetime64
        np.float32, np.float64
        np.int32, np.int64  # be with caution with int

    Also See
    --------
    pandas.read_csv

    '''
    parsed_dtypes = parse_fields(dtypes)

    dtype, parse_dates, converters, default_value_dict, field_names = parse_dtypes(parsed_dtypes)

    names = field_names if filter_names else None
    data = pd.read_csv(filename, header=header, encoding=encoding, sep=sep, 
            dtype='unicode', error_bad_lines=error_bad_lines, usecols=names, **kargs)

    ok_flag = 1
    for (name, field_type, field_parser, default) in parsed_dtypes:
        print("> check [{}]..".format(name.encode('utf8')))
        # np.datetime64  <-> np.dtype("<M8[ns]")
        if field_type == np.datetime64:
            field_type = np.dtype('<M8[ns]')
            new_col = pd.to_datetime(data[name], coerce=force_datetime_transform)
        # unicode/str <-> np.dtype('O')
        elif field_type in [unicode, str]:
            field_type = np.dtype('O')
            new_col = data[name]
        #
        else:
            new_col = data[name].astype(field_type, raise_on_error=False)

        if new_col.dtype == field_type: 
            data[name] = new_col
            continue
        else:
            print(" [Warn] use element-level transform ..")
            col = data[name]
            for index, item in enumerate(col):
                try:
                    col[index] = field_type(item)
                    ok_flag = 0
                except:
                    print("  *Error: Index[{}], Item[{}], To Type[{}]".format(
                        index, item, field_type))
    if fillna and ok_flag:
        for index_or_name, default_val in default_value_dict.iteritems():
            data[index_or_name].fillna(default_val, inplace=True)
    return data

#@add_doc(pd.read_table)
def read_table(filename, sep='\t', header=0, encoding='utf-8', filter_names=True, **kargs):
    ''' read txt table file by pd.read_table

    Also see
    --------
    read_csv(), the only difference with read_csv() is sep, that's why new version 
    pandas hasn't list this function
    '''
    return read_csv(filename, sep=sep, header=header, encoding=encoding, **kargs)






