#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, logging, time, random
from datetime import datetime
from GoogleMailer import GoogleMailer

class IpTracker:
    oldIp = ''
    userAgents = []
    sleepMultiplier = 1
    url = ''

    def __init__(self):
        logger = logging.getLogger("iplogger")
        with open("../headers/crawler-user-agents.json") as header_file:
            self.userAgents = json.load(header_file)
        
        with open("../config/url.config") as url_file:
            urlConfig = json.load(url_file)
            self.url = urlConfig['url']
            logger.debug(self.url)

    def trackIP(self):
        logger = logging.getLogger("iplogger")
        try:
            while True:
                userAgentAgency = random.choice(self.userAgents)
                userAgent = random.choice(userAgentAgency['instances'])
                logger.debug(userAgent)
                resp = requests.get(self.url, userAgent)
                currTiemstamp = datetime.now()
                status = resp.status_code
                if status == 200:
                    encoding = resp.encoding
                    currentIp = resp.text
                    ipStatus = 'idendical'
                    if(currentIp != self.oldIp):
                        ipStatus = 'new'
                        googlemailer = GoogleMailer()
                        googlemailer.mail('neue IP-Adresse: ' + currentIp, 'Der Anschluss hat eine neue IP-Adresse: ' + currentIp + '\n\nAlte IP-Adresse: ' + self.oldIp)
                        self.oldIp = currentIp
                    logger.info("[%s] IP-Address > %s ", ipStatus, currentIp)
                else:
                    logger.error("HTTP Response Status nicht ok: " + status)
                    self.ipMap[currTiemstamp] = {}
                    self.ipMap[currTiemstamp]['status'] = status
                seconds2Sleep = random.randint(5,10) * self.sleepMultiplier
                logger.info("Programm sleeps for %s seconds", seconds2Sleep)
                time.sleep(seconds2Sleep)
        except KeyboardInterrupt:
            logger.info("Schleife per STRG + C beendet")
        except Exception as ex:
            logger.info("Exception while requesting ip address status: %s", getattr(ex, 'message', str(ex)))
            googlemailer = GoogleMailer()
            msg = 'IP Tracker hat einen Fehlerfall und wurde beendet'
            googlemailer.mail(msg, msg)
        finally:
            logger.info("Programm beendet")
