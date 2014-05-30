"""
fetch a file from an HTTP (web) server over sockets via urllib;  urllib supports 
HTTP, FTP, files, and HTTPS via URL address strings;  for HTTP, the URL can name
a file or trigger a remote CGI script;  see also the urllib example in the FTP 
section, and the CGI script invocation in a later chapter;  files can be fetched 
over the net with Python in many ways that vary in code and server requirements:
over sockets, FTP, HTTP, urllib, and CGI outputs;  caveat: should run filename 
through urllib.parse.quote to escape properly unless hardcoded--see later chapters;
"""

import sys
from urllib.request import urlopen
showlines = 6
try:
    servername, filename = sys.argv[1:]              # cmdline args?
except:
    servername, filename = 'learning-python.com', '/index.html'

remoteaddr = 'http://%s%s' % (servername, filename)  # can name a CGI script too
print(remoteaddr)
remotefile = urlopen(remoteaddr)                     # returns input file object
remotedata = remotefile.readlines()                  # read data directly here
remotefile.close()
for line in remotedata[:showlines]: print(line)      # bytes with embedded \n
