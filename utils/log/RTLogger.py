#encoding:utf8
# RotateTimeLogger

import os
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


app_name = "spiderdb"
log_path = os.path.join(os.path.abspath(__file__), "./log/spiderdb/")
backupCount = 30
interval = 1
when = "midnight"

if not os.path.exists(log_path):
    os.makedirs(log_path)

SIMPLE_FORMATER = "%(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"

Rthandler = TimedRotatingFileHandler(log_path, when=when, interval=interval, backupCount=backupCount)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter(SIMPLE_FORMATER)
Rthandler.setFormatter(formatter)

logger = logging.getLogger(app_name)
logger.addHandler(Rthandler)

