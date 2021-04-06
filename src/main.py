#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import  logging, yaml, os
from logging.config import dictConfig
from IpTracker import IpTracker

if "__main__" == __name__:
    logDir = '../logs'
    if not os.path.isdir(logDir):
        os.mkdir(logDir)

    filename = 'message.log'
    if not os.path.isfile(os.path.join(logDir, filename)):
        with open(os.path.join(logDir, filename), 'w') as fp:
            pass
    
    with open("../config/logger.yml") as logger_config_file:
        dictConfig(yaml.safe_load(logger_config_file))

    logger = logging.getLogger("iplogger")

    ipTracker = IpTracker()
    ipTracker.trackIP()