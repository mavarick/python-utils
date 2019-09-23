#encoding:utf8
# RotateTimeLogger

import os
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


app_name = "spiderdb"
dir_name = "./"
log_name = "main.log"

log_path = os.path.join(os.path.dirname(__file__), dir_name)
backupCount = 30
interval = 1
when = "midnight"

if not os.path.exists(log_path):
    os.makedirs(log_path)

SIMPLE_FORMATER = "%(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"

log_name = os.path.join(log_path, log_name)
Rthandler = TimedRotatingFileHandler(log_name, when=when, interval=interval, backupCount=backupCount)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter(SIMPLE_FORMATER)
Rthandler.setFormatter(formatter)

logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO) 
logger.addHandler(Rthandler)
