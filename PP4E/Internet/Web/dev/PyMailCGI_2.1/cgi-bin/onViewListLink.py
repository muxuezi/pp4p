#!/usr/bin/python
##############################################################
# On user click of message link in main selection list;
# cgi.FieldStorage undoes any urllib escapes in the link's
# input parameters (%xx and '+' for spaces already undone);
# in 2.0 we only fetch 1 mail here, not entire list again!
# in 2.0 we also find mail's main text part intelligently
# instead of blindly displaying full text (poss attachments),
# and generate links to attachment files saved on the server;
# saved attachment files only work for 1 user and 1 message;
# most 2.0 enhancements inherited from the mailtools package;
##############################################################
     
import cgi
import commonhtml, secret
from externs import mailtools
#commonhtml.dumpstatepage(0)

def saveAttachments(message, parser, savedir='partsdownload'):
    """
    save fetched email's parts to files on
    server to be viewed in users web browser
    """
    import os
    if not os.path.exists(savedir):            # in CGI scrpt's cwd on server
        os.mkdir(savedir)                      # will open per your browser
    for filename in os.listdir(savedir):       # clean up last message: temp!
        dirpath = os.path.join(savedir, filename)
        os.remove(dirpath)
    typesAndNames = parser.saveParts(savedir, message)
    filenames = [fname for (ctype, fname) in typesAndNames]
    for filename in filenames:
        os.chmod(filename, 0666)               # some srvrs may need read/write
    return filenames
    
form = cgi.FieldStorage()
user, pswd, site = commonhtml.getstandardpopfields(form)
pswd = secret.decode(pswd)

try:
    msgnum   = form['mnum'].value                               # from url link
    parser   = mailtools.MailParser()
    fetcher  = mailtools.SilentMailFetcher(site, user, pswd)
    fulltext = fetcher.downloadMessage(int(msgnum))             # don't eval!
    message  = parser.parseMessage(fulltext)                    # email.Message
    parts    = saveAttachments(message, parser)                 # for url links 
    mtype, content = parser.findMainText(message)               # first txt part
#EXPERIMENTAL
    hdrstext = fulltext.split('\n\n')[0]                        # use blank line
    commonhtml.viewpage(                                        # encodes passwd
               msgnum, message, content, form, hdrstext, parts)
except: 
    commonhtml.errorpage('Error loading message')
