#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, smtplib, json
from email.mime.text import MIMEText

class GoogleMailer:
    empfaenger = ''
    sender = ''
    smtpserver = 'smtp.googlemail.com:587'
    smtpusername = ''
    smtppassword = ''
    useTLS = True

    def __init__(self):
        logger = logging.getLogger("iplogger")
        logger.info("init Googlemailer")
        with open("../config/email.config") as email_file:
            emailConfig = json.load(email_file)
            self.smtpusername = emailConfig['username']
            self.sender = emailConfig['username']
            self.smtppassword = emailConfig['password']
            self.empfaenger = emailConfig['target']

    def mail(self, titel, text):
        logger = logging.getLogger("iplogger")
        logger.info('Sende Mail mit neuer IP-Adresse')

        msg = MIMEText(text)
        msg['From'] = self.sender
        msg['To'] = self.empfaenger
        msg['Subject'] = titel
        server = smtplib.SMTP(self.smtpserver)

        if self.useTLS:
            server.starttls()
        if self.smtpusername != '' and self.smtppassword != '':
            server.login(self.smtpusername, self.smtppassword)
            server.sendmail(self.sender, self.empfaenger, msg.as_string())
            server.quit()
            logger.info('Mail wurde erfolgreich gesendet')
