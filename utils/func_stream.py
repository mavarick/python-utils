#encoding:utf8
#auth: mavarick
#date: {DATETIME}

"""
这个文件主要模拟函数式编程，形成一种串联的方式，更方便的对数据进行处理

如果有更好的方法，请不吝赐教 mavarick.liu@yahoo.com
"""


class FuncStream(object):
    def __init__(self, *args):
        self.args = args

    def start(self, *args):
        self.args = args
        return self

    def add_func(self, func):
        try:
            func_name = func.func_name
        except AttributeError, ex:
            # build-in functions
            func_name = func.__name__

        def new_func(*extra_args):
            self.args = [func(*(list(self.args) + list(extra_args)))]
            return self

        setattr(self, func_name, new_func)
        return self

    @property
    def value(self):
        return self.args[0]


def test():
    def sum2(x, y):
        return x + y

    def make_array(x, num):
        return [x] * num

    import math
    log = math.log
    exp = math.exp

    fs = FuncStream()
    fs.add_func(sum2)
    fs.add_func(sum)
    fs.add_func(exp)
    fs.add_func(make_array)

    print fs.start(1,2).sum2().exp().make_array(5).value
    print fs.start(1,2).sum2().exp().make_array(5).sum().value


if __name__ == "__main__":
    test()
