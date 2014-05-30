#!/usr/bin/python
###############################################################
# On submit in edit window--finish a write, reply, or forward;
# in 2.0, we reuse the send tools in mailtools to construct
# and send the message, instead of older manual string scheme;
# we also now inherit attachment composition from that module;
###############################################################
     
import cgi, sys, commonhtml, os
from externs import mailtools

def saveAttachments(form, maxattach=3, savedir='partsupload'):
    """
    save uploaded attach files in local files on
    server from which mailtools will add to mail
    """
    partnames = []
    for i in range(1, maxattach+1):
        fieldname = 'attach%d' % i
        if form.has_key(fieldname) and form[fieldname].filename:
            fileinfo = form[fieldname]                     # sent and filled?
            filedata = fileinfo.value                      # read into string
            filename = fileinfo.filename                   # client's path name
            if '\\' in filename:
                basename = filename.split('\\')[-1]        # try dos clients
            elif '/' in filename:
                basename = filename.split('/')[-1]         # try unix clients
            else:
                basename = filename                        # assume dir stripped
            pathname = os.path.join(savedir, basename)
            open(pathname, 'wb').write(filedata)
            os.chmod(pathname, 0666)                       # need for some srvrs
            partnames.append(pathname)                     # list of local paths
    return partnames                                       # gets type from name
      
#commonhtml.dumpstatepage(0)
form = cgi.FieldStorage()                      # parse form input data
attaches = saveAttachments(form)               # cgi.print_form(form) to see

# server name from module or get-style url
smtpservername = commonhtml.getstandardsmtpfields(form)
 
# parms assumed to be in form or url here
from commonhtml import getfield                # fetch value attributes
From = getfield(form, 'From')                  # empty fields may not be sent
To   = getfield(form, 'To')
Cc   = getfield(form, 'Cc')
Subj = getfield(form, 'Subject')
text = getfield(form, 'text')
if Cc == '?': Cc = ''

# tools reused from PyMailGUI
Tos = [addr.strip() for addr in To.split(';')]         # multiple recip lists
Ccs = (Cc and [addr.strip() for addr in Cc.split(';')]) or ''
extraHdrs = [('Cc', Ccs), ('X-Mailer', 'PyMailCGI2')]

sender = mailtools.SilentMailSender(smtpservername)
try:
    sender.sendMessage(From, Tos, Subj, extraHdrs, text, attaches)
except:
    commonhtml.errorpage('Send mail error')
else:
    commonhtml.confirmationpage('Send mail')
