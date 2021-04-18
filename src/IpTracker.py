#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import logging
import time
import random
from datetime import datetime
from GoogleMailer import GoogleMailer


class IpTracker:
    oldIp = ''
    url = ''
    logger = logging.getLogger("iplogger")

    def __init__(self):
        with open("../headers/crawler-user-agents.json") as header_file:
            self.userAgentAgencies = json.load(header_file)

        with open("../config/settings.config") as settings_file:
            settings = json.load(settings_file)
            self.url = settings['url']
            self.enableMailinfo = settings['enableMailinfo']
            self.sleepDuration = settings['sleepDuration']
            self.logger.debug(self.url)

    def selectUserAgent(self):
        userAgentAgency = random.choice(self.userAgentAgencies)
        userAgents = userAgentAgency['instances']
        if (len(userAgents) < 1):
            return self.selectUserAgent()
        else:
            userAgent = random.choice(userAgents)
            self.logger.debug('User-Agent: %s', userAgent)
            return userAgent

    def buildHTTPHeader(self):
        header = {}
        userAgent = self.selectUserAgent()
        header['User-Agent'] = userAgent
        self.logger.debug('Header: %s', header)
        return header

    def trackIP(self):
        try:
            while True:
                resp = requests.get(
                    self.url, self.buildHTTPHeader())
                currTiemstamp = datetime.now()
                status = resp.status_code
                if status == 200:
                    encoding = resp.encoding
                    currentIp = resp.text
                    ipStatus = 'idendical'
                    if(currentIp != self.oldIp):
                        ipStatus = 'new'
                        googlemailer = GoogleMailer()
                        if self.enableMailinfo:
                            googlemailer.mail('neue IP-Adresse: ' + currentIp, 'Der Anschluss hat eine neue IP-Adresse: ' +
                                              currentIp + '\n\nAlte IP-Adresse: ' + self.oldIp)
                        self.oldIp = currentIp
                    self.logger.info("[%s] IP-Address > %s ",
                                     ipStatus, currentIp)
                else:
                    self.logger.error(
                        "HTTP Response Status nicht ok: " + status)
                    self.ipMap[currTiemstamp] = {}
                    self.ipMap[currTiemstamp]['status'] = status
                self.logger.info(
                    "Programm sleeps for %s seconds", self.sleepDuration)
                time.sleep(self.sleepDuration)
        except KeyboardInterrupt:
            self.logger.info("Schleife per STRG + C beendet")
        except Exception as ex:
            self.logger.info("Exception while requesting ip address status: %s", getattr(
                ex, 'message', str(ex)))
            googlemailer = GoogleMailer()
            msg = 'IP Tracker hat einen Fehlerfall und wurde beendet'
            if self.enableMailinfo:
                googlemailer.mail(msg, msg)
        finally:
            self.logger.info("Programm beendet")
