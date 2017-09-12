#!/usr/bin/env python
# encoding:utf8

"""
 contains tools for hadoop commands
"""

import commands


def run_shell(cmd):
    """run shell commands, return code and result"""
    code, msg = commands.getstatusoutput(cmd)
    return code, msg


class hdptools(object):
    def __init__(self, hadoop_bin="hadoop"):
        self.hadoop_bin = hadoop_bin

    def exists_path(self, hdfs_path):
        cmd = "%s dfs -test -e %s" % (self.hadoop_bin, hdfs_path)
        code, msg = run_shell(cmd)
        # code = 0 means exists, else is not
        return code

    run_shell = run_shell

    def dir(self, path_dir):
        """list hdfs directory files"""
        cmd = "%s fs -ls %s" % (self.hadoop_bin, path_dir)
        code, msg = run_shell(cmd)
        items = []
        if code != 0 or not msg:
            return code, items
        return code, [line.split(" ")[-1] for line in msg.split("\n")[1:]]

    def dir_empty(self, path_dir):
        """ check weather dir is empty
        
        return code. code=-1, dir donot exists; else size of directory files
        """
        code, items = self.dir(path_dir)
        if code != 0:
            code = -1
        return code or len(items)




