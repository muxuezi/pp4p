import cgi, sys
form = cgi.FieldStorage()      # print all inputs to stderr; stodout=reply page
for name in form.keys():
    print('[%s:%s]' % (name, form[name].value), end=' ', file=sys.stderr)
