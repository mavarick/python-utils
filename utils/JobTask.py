#!/usr/bin/env python
# encoding:utf8

import os
import sys
import time
import pdb
import traceback

from multiprocessing import Process
from threading import Thread
from datetime import datetime, timedelta, date

from decorators import ignore_exception


class TimerCronJobProcess(object):
    ''' job timer for func starting
    :param func:
    :param args: task_id, keyword, page_num
    :param kargs:
    :param timer_options: (hour, minute, second)
    :return:
    '''
    def __init__(self, name, func, args=(), kwargs={}, hour=8, minute=0, second=0):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.task_id = self.args[0]
        self.keyword = self.args[1]
        self.page_num = self.args[2]

        self.hour = self.check_time(hour, 0, 24, 0)
        self.minute = self.check_time(minute, 0, 60, 0)
        self.second = self.check_time(second, 0, 60, 0)

        self.process = None
        self.last_running_time = None

    # # deprecated
    # def run(self):
    #     today = date.today()
    #     print >>sys.stdout, today, self.last_run_date
    #     if today != self.last_run_date:
    #         self.run_instance()

    def run_instance(self):
        self.process = Process(name=self.name, target=self.func, args=self.args, kwargs=self.kwargs)
        self.process.daemon = True
        self.last_run_date = date.today()
        self.process.start()
        return

    @property
    def is_running(self):
        if self.process and self.process.is_alive():
            return True
        return False

    # @ignore_exception
    @property
    def pid(self):
        if self.is_running:
            return self.process.pid
        return None

    def get_start_time(self):
        return "%s%s%s"%(self.hour, self.minute, self.second)

    def check_time(self, value, min, max, default):
        # to "08"/'20'
        if not value: value = 0
        try:
            value = int(value)
        except:
            value = default
        if value > max: value = max
        if value < min: value = min
        return "{0:0>2}".format(value)

    def clear(self):
        if not self.is_running:
            self.process = None

    @ignore_exception
    def shutdown(self):
        if self.is_running:
            self.process.terminate()

    def info(self):
        return "name:[%s] st:[%s]"%(self.name, self.get_start_time())


class TimerCronJobThread(object):
    ''' job timer for func starting
    :param func:
    :param args:
    :param kargs:
    :param timer_options: (hour, minute, second)
    :return:
    '''
    def __init__(self, name, func, args=(), kwargs={}, hour=8, minute=0, second=0):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.hour = self.check_time(hour, 0, 24, 0)
        self.minute = self.check_time(minute, 0, 60, 0)
        self.second = self.check_time(second, 0, 60, 0)

        self.process = None
        self.last_run_date = None
        self.today_finished = False

    def run(self):
        today = date.today()
        if today != self.last_run_date:
            self.run_instance()

    def run_instance(self):
        if not self.is_running:
            self.process = Thread(name=self.name, target=self.func, args=self.args, kwargs=self.kwargs)
            self.process.setDaemon(True)
            self.last_run_date = date.today()
            self.process.start()

    @property
    def is_running(self):
        print >>sys.stdout, ">>>>", self.process, self.process.isAlive()
        if self.process and self.process.isAlive():
            return True
        return False

    @ignore_exception
    @property
    def pid(self):
        if self.is_running:
            return self.process.pid
        return None

    def get_start_time(self):
        return "%s%s%s"%(self.hour, self.minute, self.second)

    def check_time(self, value, min, max, default):
        # to "08"/'20'
        if not value: value = 0
        try:
            value = int(value)
        except:
            value = default
        if value > max: value = max
        if value < min: value = min
        return "{0:0>2}".format(value)

    def clear(self):
        if not self.is_running:
            self.process = None

    @ignore_exception
    def shutdown(self):
        # TODO
        raise NotImplementedError("thread could not be shutdown")

    def info(self):
        return "name:[%s] st:[%s]"%(self.name, self.get_start_time())