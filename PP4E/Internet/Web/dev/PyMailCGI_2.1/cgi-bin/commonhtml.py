#!/usr/bin/python
##############################################################################
# generate standard page header, list, and footer HTML; isolates html 
# generation-related details in this file; text printed here goes over a 
# socket to the client, to create parts of a new web page in the web browser;
# uses one print per line, instead of string blocks; uses urllib to escape 
# parms in url links auto from a dict, but cgi.escape to put them in html 
# hidden fields; some of the tools here are useful outside pymailcgi; could
# also return html generated here instead of  printing it, so it could be 
# included in other pages; could also structure as a single cgi script that 
# gets and tests a next action name as a hidden form field; caveat: this 
# system works, but was largely written during a 2-hour layover at the 
# Chicago O'Hare airport: there is room for improvement and optimization;
##############################################################################
     
import cgi, urllib, sys, os
sys.stderr = sys.stdout           # show error messages in browser
from externs import mailconfig    # from a package somewhere on server
     
# my cgi address root
#urlroot = 'http://starship.python.net/~lutz/PyMailCgi/'
#urlroot = 'http://localhost:8000/cgi-bin/'

urlroot  = ''  # use minimal, relative paths
     
def pageheader(app='PyMailCGI', color='#FFFFFF', kind='main', info=''):
    print 'Content-type: text/html\n'
    print '<html><head><title>%s: %s page (PP3E)</title></head>' % (app, kind)
    print '<body bgcolor="%s"><h1>%s %s</h1><hr>' % (color, app, (info or kind))
     
def pagefooter(root='pymailcgi.html'):
    print '</p><hr><a href="http://www.python.org">'
    print '<img src="../PythonPoweredSmall.gif" '
    print 'align=left alt="[Python Logo]" border=0 hspace=15></a>' 
    print '<a href="../%s">Back to root page</a>' % root
    print '</body></html>'
     
def formatlink(cgiurl, parmdict):
    """
    make "%url?key=val&key=val" query link from a dictionary;
    escapes str() of all key and val with %xx, changes ' ' to +
    note that url escapes are different from html (cgi.escape)
    """ 
    parmtext = urllib.urlencode(parmdict)           # calls urllib.quote_plus
    return '%s?%s' % (cgiurl, parmtext)             # urllib does all the work
     
def pagelistsimple(linklist):                       # show simple ordered list
    print '<ol>'
    for (text, cgiurl, parmdict) in linklist:
        link = formatlink(cgiurl, parmdict)
        text = cgi.escape(text)
        print '<li><a href="%s">\n    %s</a>' % (link, text)
    print '</ol>'
 
def pagelisttable(linklist):                        # show list in a table
    print '<p><table border>'                       # escape text to be safe
    count = 1
    for (text, cgiurl, parmdict) in linklist:
        link = formatlink(cgiurl, parmdict)
        text = cgi.escape(text)
        print '<tr><th><a href="%s">View</a> %d<td>\n %s' % (link, count, text)
        count = count+1
    print '</table>'
     
def listpage(linkslist, kind='selection list'):
    pageheader(kind=kind)
    pagelisttable(linkslist)         # [('text', 'cgiurl', {'parm':'value'})]
    pagefooter()
     
def messagearea(headers, text, extra=''):
    print '<table border cellpadding=3>'
    for hdr in ('From', 'To', 'Cc', 'Subject'):
        val = headers.get(hdr, '?')
        val = cgi.escape(val, quote=1)
        print '<tr><th align=right>%s:' % hdr
        print '    <td><input type=text '
        print '    name=%s value="%s" %s size=60>' % (hdr, val, extra)
    print '<tr><th align=right>Text:'
    print '<td><textarea name=text cols=80 rows=10 %s>' % extra
    print '%s\n</textarea></table>' % (cgi.escape(text) or '?')   # if has </>s

def viewattachmentlinks(partnames):
    """
    create hyperlinks to locally saved part/atacment files
    when clicked, users web browser will handle opening
    assumes just one user, only valid while viewing 1 msg
    """ 
    print '<hr><table border cellpadding=3><tr><th>Parts:'
    for filename in partnames:
        basename = os.path.basename(filename)
        filename  = filename.replace('\\', '/') # windows hack
        print '<td><a href=../%s>%s</a>' % (filename, basename)
    print '</table><hr>'
    
def viewpage(msgnum, headers, text, form, hdrstext, parts=[]):
    """
    on View + select (generated link click)
    very subtle thing: at this point, pswd was url encoded in the
    link, and then unencoded by cgi input parser; it's being embedded
    in html here, so we use cgi.escape; this usually sends nonprintable
    chars in the hidden field's html, but works on ie and ns anyhow:
    in url:  ?user=lutz&mnum=3&pswd=%8cg%c2P%1e%f0%5b%c5J%1c%f3&...
    in html: <input type=hidden name=pswd value="...nonprintables..">
    could urllib.quote the html field here too, but must urllib.unquote
    in next script (which precludes passing the inputs in a URL instead 
    of the form); can also fall back on numeric string fmt in secret.py
    """ 
    pageheader(kind='View')
    user, pswd, site = map(cgi.escape, getstandardpopfields(form))
    print '<form method=get action="%sonViewPageAction.py">' % urlroot
    print '<input type=hidden name=mnum value="%s">' % msgnum
    print '<input type=hidden name=user value="%s">' % user     # from page|url
    print '<input type=hidden name=site value="%s">' % site     # for deletes
    print '<input type=hidden name=pswd value="%s">' % pswd     # pswd encoded
    messagearea(headers, text, 'readonly')
    if parts: viewattachmentlinks(parts)
     
    # onViewPageAction.quotetext needs date passed in page
    print '<input type=hidden name=Date value="%s">' % headers.get('Date','?')

#EXPERIMENTAL
    # delete needs hdrs text for inbox synch tests: can be multi-K large
    hdrstext = cgi.escape(hdrstext, quote=True)   # escape '"' too
    print '<input type=hidden name=Hdrstext value="%s">' % hdrstext
    
    print '<table><tr><th align=right>Action:'
    print '<td><select name=action>'
    print '    <option>Reply<option>Forward<option>Delete</select>'
    print '<input type=submit value="Next">'
    print '</table></form>'                      # no 'reset' needed here
    pagefooter()

def sendattachmentwidgets(maxattach=3):
    print '<p><b>Attach:</b><br>'
    for i in range(1, maxattach+1):
        print '<input size=80 type=file name=attach%d><br>' % i
    print '</p>'

def editpage(kind, headers={}, text=''):     
    # on Send, View+select+Reply, View+select+Fwd
    pageheader(kind=kind)
    print '<p><form enctype="multipart/form-data" method=post',
    print 'action="%sonEditPageSend.py">' % urlroot
    if mailconfig.mysignature:
        text = '\n%s\n%s' % (mailconfig.mysignature, text)
    messagearea(headers, text)
    sendattachmentwidgets()
    print '<input type=submit value="Send">'
    print '<input type=reset  value="Reset">'
    print '</form>'
    pagefooter()
     
def errorpage(message, stacktrace=True):
    pageheader(kind='Error')                        # was sys.exc_type/exc_value
    exc_type, exc_value, exc_tb = sys.exc_info()
    print '<h2>Error Description</h2><p>', message  
    print '<h2>Python Exception</h2><p>',  cgi.escape(str(exc_type))
    print '<h2>Exception details</h2><p>', cgi.escape(str(exc_value))
    if stacktrace:
        print '<h2>Exception traceback</h2><p><pre>'
        import traceback
        traceback.print_tb(exc_tb, None, sys.stdout)
        print '</pre>'
    pagefooter()
     
def confirmationpage(kind):
    pageheader(kind='Confirmation')
    print '<h2>%s operation was successful</h2>' % kind
    print '<p>Press the link below to return to the main page.</p>'
    pagefooter()
     
def getfield(form, field, default=''):
    # emulate dictionary get method
    return (form.has_key(field) and form[field].value) or default
     
def getstandardpopfields(form):
    """
    fields can arrive missing or '' or with a real value
    hard-coded in a url; default to mailconfig settings
    """
    return (getfield(form, 'user', mailconfig.popusername),
            getfield(form, 'pswd', '?'),
            getfield(form, 'site', mailconfig.popservername))
     
def getstandardsmtpfields(form):
    return  getfield(form, 'site', mailconfig.smtpservername)
     
def runsilent(func, args):
    """
    run a function without writing stdout
    ex: suppress print's in imported tools
    else they go to the client/browser
    """
    class Silent:
        def write(self, line): pass 
    save_stdout = sys.stdout
    sys.stdout  = Silent()                         # send print to dummy object
    try:                                           # which has a write method
        result = func(*args)                       # try to return func result
    finally:                                       # but always restore stdout
        sys.stdout = save_stdout
    return result
     
def dumpstatepage(exhaustive=0):
    """
    for debugging: call me at top of a cgi to
    generate a new page with cgi state details 
    """
    if exhaustive:
        cgi.test()                       # show page with form, environ, etc.
    else:                                
        pageheader(kind='state dump')
        form = cgi.FieldStorage()        # show just form fields names/values
        cgi.print_form(form)
        pagefooter()
    sys.exit()
                              
def selftest(showastable=False):                    # make phony web page
    links = [                                       # [(text, url, {parms})]
        ('text1', urlroot + 'page1.cgi', {'a':1}),         
        ('text2', urlroot + 'page1.cgi', {'a':2, 'b':'3'}),
        ('text3', urlroot + 'page2.cgi', {'x':'a b', 'y':'a<b&c', 'z':'?'}),
        ('te<>4', urlroot + 'page2.cgi', {'<x>':'', 'y':'<a>', 'z':None})]
    pageheader(kind='View')
    if showastable:
        pagelisttable(links)
    else:
        pagelistsimple(links)
    pagefooter()
     
if __name__ == '__main__':                          # when run, not imported
    selftest(len(sys.argv) > 1)                     # html goes to stdout
