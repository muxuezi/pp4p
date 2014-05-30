from mailconfig_book import *                 # get base in . (copied from ..)
popusername = 'lutz@learning-python.com'
myaddress   = 'Mark Lutz <lutz@learning-python.com>'  # 'lutz@learn-py.com' in book
listbg = 'wheat'                              # goldenrod, dark green, beige
listfg = 'navy'                               # chocolate, brown,...
viewbg = 'aquamarine'
viewfg = 'black'
wrapsz = 80
#viewheaders = None     # no Bcc
viewheaders = ('Bcc',)  # actually, yes
fetchlimit = 100        # load more headers
