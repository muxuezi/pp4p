#!/usr/bin/python
"""
################################################################################
On submit in edit window: finish a write, reply, or forward;

in 2.0+, we reuse the send tools in mailtools to construct and send the message,
instead of older manual string scheme;  we also inherit attachment structure
composition and MIME encoding for sent mails from that module;

3.0: CGI uploads fail in the py3.1 cgi module for binary and incompatibly-encoded 
text, so we simply use the platform default here (cgi's parser does no better);
3.0: use simple Unicode encoding rules for main text and attachments too;
################################################################################
"""

import cgi, sys, commonhtml, os
from externs import mailtools

savedir = 'partsupload'
if not os.path.exists(savedir):
    os.mkdir(savedir)

def saveAttachments(form, maxattach=3, savedir=savedir):
    """
    save uploaded attachment files in local files on server from 
    which mailtools will add to mail;  the 3.1 FieldStorage parser 
    and other parts of cgi module can fail for many upload types,
    so we don't try very hard to handle Unicode encodings here;
    """
    partnames = []
    for i in range(1, maxattach+1):
        fieldname = 'attach%d' % i
        if fieldname in form and form[fieldname].filename:
            fileinfo = form[fieldname]                     # sent and filled?
            filedata = fileinfo.value                      # read into string
            filename = fileinfo.filename                   # client's pathname
            if '\\' in filename:
                basename = filename.split('\\')[-1]        # try DOS clients
            elif '/' in filename:
                basename = filename.split('/')[-1]         # try Unix clients
            else:
                basename = filename                        # assume dir stripped
            pathname = os.path.join(savedir, basename)
            if isinstance(filedata, str):                  # 3.0: rb needs bytes
                filedata = filedata.encode()               # 3.0: use encoding?
            savefile = open(pathname, 'wb')
            savefile.write(filedata)                       # or a with statement
            savefile.close()                               # but EIBTI still
            os.chmod(pathname, 0o666)                      # need for some srvrs
            partnames.append(pathname)                     # list of local paths
    return partnames                                       # gets type from name

#commonhtml.dumpstatepage(0)
form = cgi.FieldStorage()                      # parse form input data
attaches = saveAttachments(form)               # cgi.print_form(form) to see

# server name from module or get-style URL
smtpservername = commonhtml.getstandardsmtpfields(form)

# parms assumed to be in form or URL here
from commonhtml import getfield                # fetch value attributes
From = getfield(form, 'From')                  # empty fields may not be sent
To   = getfield(form, 'To')
Cc   = getfield(form, 'Cc')
Subj = getfield(form, 'Subject')
text = getfield(form, 'text')
if Cc == '?': Cc = ''

# 3.0: headers encoded per utf8 within mailtools if non-ascii
parser = mailtools.MailParser()
Tos = parser.splitAddresses(To)                # multiple recip lists: ',' sept
Ccs = (Cc and parser.splitAddresses(Cc)) or ''
extraHdrs = [('Cc', Ccs), ('X-Mailer', 'PyMailCGI 3.0')]

# 3.0: resolve main text and text attachment encodings; default=ascii in mailtools
bodyencoding = 'ascii'
try:
    text.encode(bodyencoding)          # try ascii first (or latin-1?)
except (UnicodeError, LookupError):    # else use tuf8 as fallback (or config?)
    bodyencoding = 'utf-8'             # tbd: this is more limited than PyMailGUI

# 3.0: use utf8 for all attachments; we can't ask here
attachencodings = ['utf-8'] * len(attaches)    # ignored for non-text parts

# encode and send
sender = mailtools.SilentMailSender(smtpservername)
try:
    sender.sendMessage(From, Tos, Subj, extraHdrs, text, attaches,
                                           bodytextEncoding=bodyencoding,
                                           attachesEncodings=attachencodings)
except:
    commonhtml.errorpage('Send mail error')
else:
    commonhtml.confirmationpage('Send mail')
