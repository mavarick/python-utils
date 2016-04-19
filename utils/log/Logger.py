#!/usr/bin/env python
#encoding:utf8

"""功能：
实现代码级别的logger功能，包括：
1，修改日志存放位置；
2，更改日志存储方式；按天等等


usage:
 for rotateing time handler
>>
logger = init_logger("isite-alexa", handler_names=['rtfile'],
                    logger_parameters=dict(log_path="./log/isite.alexa.log"))
#then use code like below to pop out loggers
logger.info("log info")
"""

import pdb
import copy

import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

###############################################################################
# TODO, Default Values
# console, rfile, rtfile
# handler_name = "console"
# handler_name = "rtfile"
global_handler_names = ["rtfile"]
# for formatter
logger_formater = "detail"  # empty, simple, detail. TODO, all is detail now!
# for detail information of configuration
global_logger_parameters = {
    "log_path": "./log/run.log",
    "backupCount": 30,
    "interval": 1,
    "when": "midnight",
    'level': logging.NOTSET  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

###############################################################################
# TODO. level
NOSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR

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
}.get(logger_formater, EMPTY_FORMATER)


handler_names = set()
LOGGER_HANDLER_DICT = {}


def get_console_handler(*args, **kwargs):
    level = kwargs.get("level", logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(FORMATER)
    ch.setFormatter(formatter)
    return ch
handler_name = "console"
handler_names.add(handler_name)
LOGGER_HANDLER_DICT[handler_name] = get_console_handler


def get_rfile_handler(*args, **kwargs):
    log_path = kwargs.get("log_path", "./run.log")
    backupCount = kwargs.get("backupCount", 30)
    maxBytes = kwargs.get("maxBytes", 10*1024*1024)
    level = kwargs.get("level", logging.INFO)

    Rthandler = RotatingFileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
    Rthandler.setLevel(level)
    formatter = logging.Formatter(FORMATER)
    Rthandler.setFormatter(formatter)
    return Rthandler
handler_name = "rfile"
handler_names.add(handler_name)
LOGGER_HANDLER_DICT[handler_name] = get_rfile_handler


def get_rtfile_handler(*args, **kwargs):
    log_path = kwargs.get("log_path", "./run.log")
    backupCount = kwargs.get("backupCount", 30)
    interval = kwargs.get("interval", 1)
    when = kwargs.get("when", "midnight")
    level = kwargs.get("level", logging.INFO)

    Rthandler = TimedRotatingFileHandler(log_path, when=when, interval=interval, backupCount=backupCount)
    Rthandler.setLevel(level)
    formatter = logging.Formatter(FORMATER)
    Rthandler.setFormatter(formatter)
    return Rthandler
handler_name = "rtfile"
handler_names.add(handler_name)
LOGGER_HANDLER_DICT[handler_name] = get_rtfile_handler


def init_logger(name, handler_names=global_handler_names, level=logging.INFO,
                logger_parameters={}):
    """
    :param name: Logger name, default is 'root'
    :param handler_names:  console, rfile, rtfile, default is rtfile
    :param level: default is logger.INFO
    :param logger_parameters:
    :return:
    """
    _logger = logging.getLogger(name)
    _logger.setLevel(level)
    parameters = copy.copy(global_logger_parameters)
    parameters.update(logger_parameters)
    parameters['level'] = level
    for handler_name in handler_names:
        assert handler_name in handler_names, \
            "logger name[%s] must be one of [%s]"%(handler_name, ','.join(handler_names))
        handler = LOGGER_HANDLER_DICT[handler_name](**parameters)
        _logger.addHandler(handler)
    return _logger


if __name__ == "__main__":
    logger_parameters = dict(log_path="./log/run.test.log")
    logger = init_logger("test", handler_names=['rtfile'],
                         logger_parameters=logger_parameters)
    logger.info("ttttttt")
    # logger.warning("ttttttt")

