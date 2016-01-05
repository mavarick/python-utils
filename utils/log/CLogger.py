#!/usr/bin/env python
#encoding:utf8

"""功能：
实现代码级别的logger功能，包括：
1，修改日志存放位置；
2，更改日志存储方式；按天等等

"""
import pdb

import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

###############################################################################
# console, rfile, rtfile

# LOGGER_NAME = "console"

# LOGGER_NAME = "rtfile"
logger_names = ["console", "rfile"]
# for formatter
formater = "detail"  # empty, simple, detail
# for detail information of configuration
logger_info = {
    "log_path": "./run.log",
    "backupCount": 30,
    "interval": 1,
    "when": "midnight",
    'level': logging.NOTSET  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

###############################################################################
# logger without configure file
EMPTY_FORMATER = ""  # used to simply print log info
DETAIL_FORMATER = "%(asctime)s %(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"
SIMPLE_FORMATER = "%(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"
# FORMATER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


FORMATER = {
    "empty": EMPTY_FORMATER,
    "simple": SIMPLE_FORMATER,
    "detail": DETAIL_FORMATER
}.get(formater, EMPTY_FORMATER)


LOGGER_NAMES = set()
LOGGER_HANDLER_DICT = {}

logger_name = "console"
def get_console_handler(*args, **kargs):
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMATER)
    ch.setFormatter(formatter)
    return ch
LOGGER_NAMES.add(logger_name)
LOGGER_HANDLER_DICT[logger_name] = get_console_handler


logger_name = "rfile"
def get_rfile_handler(*args, **kwargs):
    log_path = kwargs.get("log_path", "./run.log")
    backupCount = kwargs.get("backupCount", 30)
    maxBytes = kwargs.get("maxBytes", 10*1024*1024)

    Rthandler = RotatingFileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMATER)
    Rthandler.setFormatter(formatter)
    return Rthandler
LOGGER_NAMES.add(logger_name)
LOGGER_HANDLER_DICT[logger_name] = get_rfile_handler


logger_name = "rtfile"
def get_rtfile_handler(*args, **kwargs):
    log_path = kwargs.get("log_path", "./run.log")
    backupCount = kwargs.get("backupCount", 30)
    interval = kwargs.get("interval", 1)
    when = kwargs.get("when", "midnight")

    Rthandler = TimedRotatingFileHandler(log_path, when=when, interval=interval, backupCount=backupCount)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMATER)
    Rthandler.setFormatter(formatter)
    return Rthandler
LOGGER_NAMES.add(logger_name)
LOGGER_HANDLER_DICT[logger_name] = get_rtfile_handler


def init_logger(logger_names, level=logging.INFO, **kargs):
    '''
    params:: log_path: string. for log: rfile, rtfile.
    params:: backupCount: int. for rfile, rtfile.
    params:: maxBytes: for rfile.
    params:: interval: for rtfile.
    params:: when: for rtfile
    '''
    _logger = logging.getLogger()
    _logger.setLevel(level)
    for logger_name in logger_names:
        assert logger_name in LOGGER_NAMES, \
            "logger name[%s] must be one of [%s]"%(logger_name, ','.join(LOGGER_NAMES))
        handler = LOGGER_HANDLER_DICT[logger_name](**kargs)
        _logger.addHandler(handler)
    return _logger


logger = init_logger(logger_names, **logger_info)

if not logger:
    raise Exception("logger is None")

if __name__ == "__main__":
    logger.info("ttttttt")
    # logger.warning("ttttttt")

