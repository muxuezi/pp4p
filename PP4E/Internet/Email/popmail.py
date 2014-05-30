#!/usr/local/bin/python
"""
##############################################################################
use the Python POP3 mail interface module to view your POP email account
messages;  this is just a simple listing--see pymail.py for a client with
more user interaction features, and smtpmail.py for a script which sends
mail;  POP is used to retrieve mail, and runs on a socket using port number
110 on the server machine, but Python's poplib hides all protocol details;
to send mail, use the smtplib module (or os.popen('mail...')).  see also:
imaplib module for IMAP alternative, PyMailGUI/PyMailCGI for more features; 
##############################################################################
"""

import poplib, getpass, sys, mailconfig

mailserver = mailconfig.popservername      # ex: 'pop.rmi.net'
mailuser   = mailconfig.popusername        # ex: 'lutz'
mailpasswd = getpass.getpass('Password for %s?' % mailserver)

print('Connecting...')
server = poplib.POP3(mailserver)
server.user(mailuser)                      # connect, log in to mail server
server.pass_(mailpasswd)                   # pass is a reserved word

try:
    print(server.getwelcome())             # print returned greeting message
    msgCount, msgBytes = server.stat()
    print('There are', msgCount, 'mail messages in', msgBytes, 'bytes')
    print(server.list())
    print('-' * 80)
    input('[Press Enter key]')

    for i in range(msgCount):
        hdr, message, octets = server.retr(i+1)    # octets is byte count
        for line in message: print(line.decode())  # retrieve, print all mail
        print('-' * 80)                            # mail text is bytes in 3.x
        if i < msgCount - 1:
           input('[Press Enter key]')              # mail box locked till quit
finally:                                           # make sure we unlock mbox
    server.quit()                                  # else locked till timeout
print('Bye.')
