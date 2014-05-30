#!/usr/local/bin/python
"""
same, but allow To: header to be input to mask true recipients;
the From: header already can differ from the actuial sender;
"""

import smtplib, sys, email.utils, mailconfig
mailserver = mailconfig.smtpservername         # ex: smtp.rmi.net

From = input('From? ').strip()                 # or import from mailconfig
To   = input('To?   ').strip()                 # ex: python-list@python.org
Tos  = To.split(';')                           # allow a list of recipients
Subj = input('Subj? ').strip()
Date = email.utils.formatdate()                # curr datetime, rfc2822

# standard headers, followed by blank line, followed by text
text = ('From: %s\nDate: %s\nSubject: %s\n' % (From, Date, Subj))   # DIFFERS

print('Type message text, end with line=[Ctrl+d (Unix), Ctrl+z (Windows)]')
while True:
    line = sys.stdin.readline()
    if not line: 
        break                        # exit on ctrl-d/z
   #if line[:4] == 'From':
   #    line = '>' + line            # servers may escape
    text += line

print('Connecting...')
server = smtplib.SMTP(mailserver)              # connect, no log-in step
failed = server.sendmail(From, Tos, text)
server.quit()
if failed:                                     # smtplib may raise exceptions
    print('Failed recipients:', failed)        # too, but let them pass here
else:
    print('No errors.')
print('Bye.')
