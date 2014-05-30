import sys, os
savename = 'test-cgi-uploads-bug2.bin'  # with multiple files in HTML form

print("Content-type: text/html\n") 
print('<P>Content-type: '   + os.environ.get('CONTENT_TYPE'))
print('<P>Content-length: ' + os.environ.get('CONTENT_LENGTH'))

fp = open(sys.stdin.fileno(), 'rb')     # read in binary mode to avoid decoding
data = fp.read()                        # don't parse with FieldStorage, same reason
open(savename, 'wb').write(data)        # write in binary mode as raw bytes
print('<P>Done: see %s for input data' % savename)