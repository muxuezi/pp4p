###################################################################
# mail list loader; future--change me to save mail list between
# cgi script runs, to avoid reloading all mail each time; this
# won't impact clients that use the interfaces here if done well;
# for now, to keep this simple, reloads all mail for each list page;
# 2.0: we now only load message headers (via TOP), not full msg,
# but still fetch all hdrs for each index list--in-memory caches
# don't work in a stateless CGI script, and require a real db;
###################################################################
     
from commonhtml import runsilent         # suppress print's (no verbose flag)
from externs    import mailtools         # shared with PyMailGUI
     
# load all mail from number 1 up
# this may trigger an exception

import sys
def progress(*args):  # not used
    sys.stderr.write(str(args) + '\n')

def loadmailhdrs(mailserver, mailuser, mailpswd):
    fetcher = mailtools.SilentMailFetcher(mailserver, mailuser, mailpswd)
    hdrs, sizes, full = fetcher.downloadAllHeaders()     # get list of hdr text
    return hdrs
