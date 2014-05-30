#!/usr/local/bin/python
"""
A Python script to download a file by FTP by its URL string; use higher-level
urllib instead of ftplib to fetch file;  urllib supports FTP, HTTP, client-side
HTTPS, and local files, and handles proxies, redirects, cookies, and more;
urllib also allows downloads of html pages, images, text, etc.;  see also 
Python html/xml parsers for web pages fetched by urllib in Chapter 19;
"""

import os, getpass
from urllib.request import urlopen       # socket-based web tools
filename = 'monkeys.jpg'                 # remote/local filename
password = getpass.getpass('Pswd?')

remoteaddr = 'ftp://lutz:%s@ftp.rmi.net/%s;type=i' % (password, filename)
print('Downloading', remoteaddr)

# this works too:
# urllib.request.urlretrieve(remoteaddr, filename)

remotefile = urlopen(remoteaddr)                 # returns input file-like object
localfile  = open(filename, 'wb')                # where to store data locally
localfile.write(remotefile.read())
localfile.close()
remotefile.close()
