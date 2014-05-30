#!/usr/bin/python
#######################################################################
# On submit in mail view window, action selected=(fwd, reply, delete)
# in 2.0, we reuse the mailtools delete logic orig coded for PyMailGUI
#######################################################################
     
import cgi, commonhtml, secret
from   externs import mailtools, mailconfig
from   commonhtml import getfield

def quotetext(form):
    """
    note that headers come from the prior page's form here,
    not from parsing the mail message again; that means that 
    commonhtml.viewpage must pass along date as a hidden field
    """ 
    quoted = '\n-----Original Message-----\n'
    for hdr in ('From', 'To', 'Date'):
        quoted = quoted + '%s: %s\n' % (hdr, getfield(form, hdr))
    quoted = quoted + '\n' +   getfield(form, 'text')
    quoted = '\n' + quoted.replace('\n', '\n> ')
    return quoted

form = cgi.FieldStorage()  # parse form or url data
user, pswd, site = commonhtml.getstandardpopfields(form)
pswd = secret.decode(pswd)
     
try:
    if form['action'].value   == 'Reply':
        headers = {'From':    mailconfig.myaddress,
                   'To':      getfield(form, 'From'),
                   'Cc':      mailconfig.myaddress,
                   'Subject': 'Re: ' + getfield(form, 'Subject')}
        commonhtml.editpage('Reply', headers, quotetext(form))
     
    elif form['action'].value == 'Forward':
        headers = {'From':    mailconfig.myaddress,
                   'To':      '',
                   'Cc':      mailconfig.myaddress,
                   'Subject': 'Fwd: ' + getfield(form, 'Subject')}
        commonhtml.editpage('Forward', headers, quotetext(form))
        
    elif form['action'].value == 'Delete':     # mnum field is required here
        msgnum  = int(form['mnum'].value)      # but not eval(): may be code
        fetcher = mailtools.SilentMailFetcher(site, user, pswd)
#EXPERIMENTAL
        #fetcher.deleteMessages([msgnum])
        hdrstext = getfield(form, 'Hdrstext') + '\n'          
        hdrstext = hdrstext.replace('\r\n', '\n')             # get \n from top
        dummyhdrslist = [None] * msgnum                       # only one msg hdr
        dummyhdrslist[msgnum-1] = hdrstext                    # in hidden field
        fetcher.deleteMessagesSafely([msgnum], dummyhdrslist) # exc on synch err
        commonhtml.confirmationpage('Delete')
     
    else:
       assert False, 'Invalid view action requested'
except:
    commonhtml.errorpage('Cannot process view action')
