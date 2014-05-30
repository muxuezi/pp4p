above = open('../mailconfig.py').read()       # copy version above here (hack?)
open('mailconfig_book.py', 'w').write(above)  # used for 'book' and as others' base
acct = input('Account name?')                 # book, rmi, train
exec('from mailconfig_%s import *' % acct)    # . is first on sys.path
