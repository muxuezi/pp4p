#!/usr/local/bin/python
"""
###########################################################################
use the Python SMTP mail interface module to send email messages; this
is just a simple one-shot send script--see pymail, PyMailGUI, and
PyMailCGI for clients with more user interaction features; also see
popmail.py for a script that retrieves mail, and the mailtools pkg
for attachments and formatting with the standard library email package;
###########################################################################
"""

import smtplib, sys, email.utils, mailconfig
mailserver = mailconfig.smtpservername         # ex: smtp.rmi.net

From = input('From? ').strip()                 # or import from mailconfig
To   = input('To?   ').strip()                 # ex: python-list@python.org
Tos  = To.split(';')                           # allow a list of recipients
Subj = input('Subj? ').strip()
Date = email.utils.formatdate()                # curr datetime, rfc2822

# standard headers, followed by blank line, followed by text
text = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n' % (From, To, Date, Subj))

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
