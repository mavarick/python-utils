#encoding:utf8

import commands

class ShellRunner(object):
    @staticmethod
    def run(cmd):
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            raise ShellRunnerException(output)
        return output


class ShellRunnerException(Exception):
    pass

