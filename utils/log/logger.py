#!/usr/bin/env python
#encoding:utf8

""" logger 

NEED TO BE TESTED
"""

import sys
import logging
import logging.config

################################################################################################
# logger without configure file
#DETAIL_FORMATER = "%(asctime)s %(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"
#SIMPLE_FORMATER = "%(levelname)-8s %(name)s[%(filename)s: %(lineno)3d]: %(message)s"
#
#Logger = logging.getLogger("DEBUG")
#console_handler = logging.StreamHandler(sys.stdout)
#formatter = logging.Formatter(SIMPLE_FORMATER)
#
#console_handler.setFormatter(formatter)
#Logger.addHandler(console_handler)
#Logger.setLevel(logging.INFO)

################################################################################################
# logger with configure file
import os
import sys

logger_name = "debug"
dir_name = os.path.dirname(os.path.abspath(__file__))
print "logging configuration base path:", dir_name
print "logging: [%s]"%logger_name

log_config_file = os.path.join(dir_name, "log.conf")

logging.config.fileConfig(log_config_file)

logger = logging.getLogger(logger_name)

# How to set log data's directory????????, TODO

if __name__ == "__main__":
    print "test"
    logger.info("this is one test")
    logger.debug("this is one test")
