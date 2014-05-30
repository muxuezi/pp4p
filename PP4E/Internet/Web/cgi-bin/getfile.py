#!/usr/bin/python
"""
##################################################################################
Display any CGI (or other) server-side file without running it. The filename can
be passed in a URL param or form field (use "localhost" as the server if local):

    http://servername/cgi-bin/getfile.py?filename=somefile.html
    http://servername/cgi-bin/getfile.py?filename=cgi-bin\somefile.py
    http://servername/cgi-bin/getfile.py?filename=cgi-bin%2Fsomefile.py

Users can cut-and-paste or "View Source" to save file locally.  On IE, running the
text/plain version (formatted=False) sometimes pops up Notepad, but end-lines are 
not always in DOS format;  Netscape shows the text correctly in the browser page 
instead.  Sending the file in text/HTML mode works on both browsers--text is 
displayed in the browser response page correctly. We also check the filename here 
to try to avoid showing private files; this may or may not prevent access to such 
files in general: don't install this script if you can't otherwise secure source!
##################################################################################
"""

import cgi, os, sys
formatted = True                                  # True=wrap text in HTML
privates  = ['PyMailCgi/cgi-bin/secret.py']       # don't show these

try:
    samefile = os.path.samefile                   # checks device, inode numbers
except:
    def samefile(path1, path2):                   # not available on Windows
        apath1 = os.path.abspath(path1).lower()   # do close approximation
        apath2 = os.path.abspath(path2).lower()   # normalizes path, same case
        return apath1 == apath2

html = """
<html><title>Getfile response</title>
<h1>Source code for: '%s'</h1>
<hr>
<pre>%s</pre>
<hr></html>"""

def restricted(filename):
    for path in privates:
        if samefile(path, filename):           # unify all paths by os.stat
            return True                        # else returns None=false

try:
    form = cgi.FieldStorage()
    filename = form['filename'].value          # URL param or form field
except:
    filename = 'cgi-bin\getfile.py'            # else default filename

try:
    assert not restricted(filename)            # load unless private
    filetext = open(filename).read()           # platform unicode encoding
except AssertionError:
    filetext = '(File access denied)'
except:
    filetext = '(Error opening file: %s)' % sys.exc_info()[1]

if not formatted:
    print('Content-type: text/plain\n')        # send plain text
    print(filetext)                            # works on NS, not IE?
else:
    print('Content-type: text/html\n')         # wrap up in HTML
    print(html % (filename, cgi.escape(filetext)))
