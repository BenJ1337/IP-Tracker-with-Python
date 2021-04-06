#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import  logging, yaml
from logging.config import dictConfig
from IpTracker import IpTracker

print("Start")
with open("../config/logger.yml") as logger_config_file:
    dictConfig(yaml.safe_load(logger_config_file))

logger = logging.getLogger("iplogger")

if "__main__" == __name__:
    ipTracker = IpTracker()
    ipTracker.trackIP()

