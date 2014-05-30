#!/usr/bin/python
"""
##################################################################################
extract file uploaded by HTTP from web browser;  users visit putfile.html to 
get the upload form page, which then triggers this script on server;  this is
very powerful, and very dangerous: you will usually want to check the filename, 
etc;  this may only work if file or dir is writable: a Unix 'chmod 777 uploads'
may suffice;  file pathnames may arrive in client's path format: handle here;

caveat: could open output file in text mode to wite receiving platform's line
ends since file content always str from the cgi module, but this is a temporary 
solution anyhow--the cgi module doesn't handle binary file uploads in 3.1 at all;
##################################################################################
"""

import cgi, os, sys
import posixpath, ntpath, macpath      # for client paths
debugmode    = False                   # True=print form info
loadtextauto = False                   # True=read file at once
uploaddir    = './uploads'             # dir to store files

sys.stderr = sys.stdout                # show error msgs
form = cgi.FieldStorage()              # parse form data
print("Content-type: text/html\n")     # with blank line
if debugmode: cgi.print_form(form)     # print form fields

# html templates

html = """
<html><title>Putfile response page</title>
<body>
<h1>Putfile response page</h1>
%s
</body></html>"""

goodhtml = html % """
<p>Your file, '%s', has been saved on the server as '%s'.
<p>An echo of the file's contents received and saved appears below.
</p><hr>
<p><pre>%s</pre>
</p><hr>
"""

# process form data

def splitpath(origpath):                              # get file at end
    for pathmodule in [posixpath, ntpath, macpath]:   # try all clients
        basename = pathmodule.split(origpath)[1]      # may be any server
        if basename != origpath:
            return basename                           # lets spaces pass
    return origpath                                   # failed or no dirs

def saveonserver(fileinfo):                           # use file input form data
    basename = splitpath(fileinfo.filename)           # name without dir path
    srvrname = os.path.join(uploaddir, basename)      # store in a dir if set
    srvrfile = open(srvrname, 'wb')                   # always write bytes here 
    if loadtextauto:
        filetext = fileinfo.value                     # reads text into string
        if isinstance(filetext, str):                 # Python 3.1 hack
            filedata = filetext.encode()
        srvrfile.write(filedata)                      # save in server file
    else:                                             # else read line by line
        numlines, filetext = 0, ''                    # e.g., for huge files
        while True:                                   # content always str here
            line = fileinfo.file.readline()           # or for loop and iterator
            if not line: break
            if isinstance(line, str):                 # Python 3.1 hack
                line = line.encode()
            srvrfile.write(line)
            filetext += line.decode()                 # ditto
            numlines += 1
        filetext = ('[Lines=%d]\n' % numlines) + filetext
    srvrfile.close()
    os.chmod(srvrname, 0o666)   # make writable: owned by 'nobody'
    return filetext, srvrname

def main():
    if not 'clientfile' in form:
        print(html % 'Error: no file was received')
    elif not form['clientfile'].filename:
        print(html % 'Error: filename is missing')
    else:
        fileinfo = form['clientfile']
        try:
            filetext, srvrname = saveonserver(fileinfo)
        except:
            errmsg = '<h2>Error</h2><p>%s<p>%s' % tuple(sys.exc_info()[:2])
            print(html % errmsg)
        else:
            print(goodhtml % (cgi.escape(fileinfo.filename),
                              cgi.escape(srvrname),
                              cgi.escape(filetext)))
main()
