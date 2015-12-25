#!/usr/bin/env python
#encoding:utf8

"""功能：
实现代码级别的logger功能，包括：
1，修改日志存放位置；
2，更改日志存储方式；按天等等

"""

import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

###############################################################################
# console, rfile, rtfile
LOGGER_NAME = "console"
# LOGGER_NAME = "rfile"

# set parameters, if use `rfile`, `rtfile`
LOG_PATH = "./run.log"
LOG_FILE_CNT = 30

###############################################################################

# logger without configure file
DETAIL_FORMATER = "%(asctime)s %(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"
SIMPLE_FORMATER = "%(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"
# FORMATER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

CONSOLE_LOGGER_NAME = "console"      # console
ROTATING_FILE_LOGGER_NAME = 'rfile'  # rotate file

# logging.basicConfig(level=logging.DEBUG,
                # format=DETAIL_FORMATER,
                # datefmt='%Y-%m-%d %H:%M:%S',  #'%a, %d %b %Y %H:%M:%S',
                # filename='run.log',
                # filemode='w'
# )

def initiate_console_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # def initiate_console_logger(logger_name):
    ch = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(DETAIL_FORMATER)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


def initiate_rfile_logger(logger_name, **kargs):
    '''
    params :: log_path, log path
    params :: bak_log_cnt，log file cnt
    '''
    log_path = kargs.get("log_path", "./run.log")
    bak_log_cnt = kargs.get("bak_log_cnt", 30)

    Rthandler = RotatingFileHandler(log_path, maxBytes=10*1024*1024,backupCount=bak_log_cnt)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter(DETAIL_FORMATER)
    Rthandler.setFormatter(formatter)
    logger = logging.getLogger(ROTATING_FILE_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(Rthandler)
    return logger


def initiate_rtfile_logger(logger_name, **kargs):
    ''' rotated file handler
    params :: log_path, log path
    params :: bak_log_cnt，log file cnt
    '''
    log_path = kargs.get("log_path", "./run.log")
    bak_log_cnt = kargs.get("bak_log_cnt", 30)

    Rthandler = TimedRotatingFileHandler(log_path, when="midnight", interval=1, backupCount=bak_log_cnt)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter(DETAIL_FORMATER)
    Rthandler.setFormatter(formatter)
    logger = logging.getLogger(ROTATING_FILE_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(Rthandler)
    return logger


if LOGGER_NAME == "console":
    logger = initiate_console_logger(LOGGER_NAME)
elif LOGGER_NAME == "rfile":
    logger = initiate_rfile_logger(LOGGER_NAME, log_path=LOG_PATH, bak_log_cnt=LOG_FILE_CNT)
elif LOGGER_NAME == 'rtfile':
    logger = initiate_rtfile_logger(LOGGER_NAME, log_path=LOG_PATH, bak_log_cnt=LOG_FILE_CNT)

if __name__ == "__main__":
    logger.info("ttttttt")
    logger.warning("ttttttt")

