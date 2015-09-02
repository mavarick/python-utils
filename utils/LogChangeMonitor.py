#!/usr/bin/env python
#encoding:utf8

'''
    monitor the log content adding data
Remainning problems:
    tail -f 
'''
import os
import subprocess

class LogMonitor(object):
    def __init__(self, filepath):
        self.file = filepath
        self.interval = 1    # interval time for monitor
        
        self.is_exist()

    def is_exist(self):
        '''
        check if the file exists
        '''
        if not os.path.exists(self.file):
            raise Exception("FileNotExistError: filename: {0}".format(self.file))

    def monitor(self):
        popen = subprocess.Popen("tail -f {0}".format(self.file), 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
        print "pid:", popen.pid
        while 1:
            line = popen.stdout.readline().strip()
            print line

        


