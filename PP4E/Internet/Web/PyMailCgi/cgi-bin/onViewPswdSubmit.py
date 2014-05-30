#!/usr/bin/python
"""
################################################################################
On submit in POP password input window: make mail list view page;

in 2.0+ we only fetch mail headers here, and fetch 1 full message later upon 
request; we still fetch all headers each time the index page is made: caching 
Messages would require a server-side(?) database and session key, or other;
3.0: decode headers for list display, though printer and browser must handle;
################################################################################
"""

import cgi
import loadmail, commonhtml
from   externs import mailtools
from   secret  import encode       # user-defined encoder module
MaxHdr = 35                        # max length of email hdrs in list

# only pswd comes from page here, rest usually in module
formdata = cgi.FieldStorage()
mailuser, mailpswd, mailsite = commonhtml.getstandardpopfields(formdata)
parser = mailtools.MailParser()

try:
    newmails = loadmail.loadmailhdrs(mailsite, mailuser, mailpswd)
    mailnum  = 1
    maillist = []                                           # or use enumerate()
    for mail in newmails:                                   # list of hdr text
        msginfo = []
        hdrs = parser.parseHeaders(mail)                    # email.message.Message
        addrhdrs = ('From', 'To', 'Cc', 'Bcc')              # decode names only
        for key in ('Subject', 'From', 'Date'):
            rawhdr = hdrs.get(key, '?')
            if key not in addrhdrs:
                dechdr = parser.decodeHeader(rawhdr)        # 3.0: decode for display
            else:                                           # encoded on sends
                dechdr = parser.decodeAddrHeader(rawhdr)    # email names only 
            msginfo.append(dechdr[:MaxHdr])
        msginfo = ' | '.join(msginfo)
        maillist.append((msginfo, commonhtml.urlroot + 'onViewListLink.py',
                                      {'mnum': mailnum,
                                       'user': mailuser,          # data params
                                       'pswd': encode(mailpswd),  # pass in URL
                                       'site': mailsite}))        # not inputs
        mailnum += 1
    commonhtml.listpage(maillist, 'mail selection list')
except:
    commonhtml.errorpage('Error loading mail index')
