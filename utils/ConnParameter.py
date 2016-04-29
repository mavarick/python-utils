# encoding:utf8

import copy


class ConnParameter(object):
    # 利用函数式编程来来操作参数,来使得程序看起来优雅
    def __init__(self, default_parameters, created=True):
        if created:
            self.parameters = copy.copy(default_parameters)
        else:
            self.parameters = default_parameters

    def update(self, **kwargs):
        self.parameters.update(kwargs)
        return self

    def __getitem__(self, item):
        return self.parameters[item]

    def get(self, item, default=None):
        return self.parameters.get(item, default)


""" USAGE
mysql_info = {
    "host": "10.44.165.50",
    "port": 3306,
    "user": "root",
    "passwd": "",
    "db": "",
    "table_name": ""
}

mysql_parameter = ConnParameter(mysql_info)

# when you want to change the parameters
cp = mysql_parameter.update(db="spider", table_name="wiki_tbl")

print "db >>",cp['db']
print "user >>", cp['user']

"""