#!/usr/bin/env python
# encoding: utf-8
"""
messaging.py

Created by Brant Faircloth on 2009-02-15.
Copyright (c) 2009 Brant Faircloth. All rights reserved.
"""

import smtplib
from time import strftime
from email.mime.text import MIMEText

def send(fromAddy, toAddy, server, user, password, msg):
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    server.sendmail(fromAddy,toAddy, msg.as_string())
    server.quit()

def completion(fromAddy, toAddy, server, user, password):
    '''send a text message indicating completion of a run'''
    text = (('Run completed at %s') % (strftime("%Y-%m-%d %H:%M:%S")))
    msg = MIMEText(text)
    msg['Subject'] = 'Run Completion'
    msg['From'] = fromAddy
    msg['To'] = toAddy
    send(fromAddy, toAddy, server, user, password, msg)
    
def alert(fromAddy, toAddy, server, user, password):
    '''send a text message indicating completion of a run'''
    text = (('A problem has occured during your run at %s') % (strftime("%Y-%m-%d %H:%M:%S")))
    msg = MIMEText(text)
    msg['Subject'] = 'Run Alert'
    msg['From'] = fromAddy
    msg['To'] = toAddy
    send(fromAddy, toAddy, server, user, password, msg)

def main():
    pass


if __name__ == '__main__':
    main()

