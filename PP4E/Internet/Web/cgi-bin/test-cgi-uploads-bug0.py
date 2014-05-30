import sys, cgi

print("Content-type: text/html\n")    #print(cgi.escape( str(type(sys.stdin.read())) ))
sys.stderr = sys.stdout               # route errors to reply page
print("<pre>")

fp = open(sys.stdin.fileno(), 'rb')   #print(cgi.escape( str(type( fp.read() )) ))
form = cgi.FieldStorage(fp)   # binary mode doesn't help: cgi+email.parser needs str

fileinfo = form['clientfile']
print(cgi.escape(fileinfo.value))     # show file if worked
