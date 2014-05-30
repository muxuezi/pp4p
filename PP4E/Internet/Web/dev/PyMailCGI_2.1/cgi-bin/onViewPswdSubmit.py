#!/usr/bin/python
############################################################
# On submit in pop password input window--make view list;
# in 2.0 we only fetch mail headers here, and fetch 1 full
# message later upon request; we still fetch all headers
# each time the index page is made: caching requires a db;
############################################################
     
import cgi
import loadmail, commonhtml
from   externs import mailtools
from   secret  import encode       # user-defined encoder module
MaxHdr = 35                        # max length of email hdrs in list
     
# only pswd comes from page here, rest usually in module
formdata = cgi.FieldStorage()
mailuser, mailpswd, mailsite = commonhtml.getstandardpopfields(formdata)
     
try:
    newmails = loadmail.loadmailhdrs(mailsite, mailuser, mailpswd)
    mailnum  = 1
    maillist = []
    for mail in newmails:                                   # list of hdr text
        msginfo = []
        hdrs = mailtools.MailParser().parseHeaders(mail)    # email.Message
        for key in ('Subject', 'From', 'Date'):
            msginfo.append(hdrs.get(key, '?')[:MaxHdr])
        msginfo = ' | '.join(msginfo)
        maillist.append((msginfo, commonhtml.urlroot + 'onViewListLink.py', 
                                      {'mnum': mailnum,
                                       'user': mailuser,          # data params
                                       'pswd': encode(mailpswd),  # pass in url
                                       'site': mailsite}))        # not inputs
        mailnum += 1
    commonhtml.listpage(maillist, 'mail selection list')
except:
    commonhtml.errorpage('Error loading mail index')
