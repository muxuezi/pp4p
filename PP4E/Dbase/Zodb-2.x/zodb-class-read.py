########################################################################
# read, update class instances in db; changing immutables like
# lists and dictionaries in-place does not update the db automatically
########################################################################

mydbfile = 'data/class.fs'
from zodb_class_make import connectdb
root, storage = connectdb(mydbfile)

# this updates db: attrs changed in method
print 'pp3e url:', root['pp3e'].url
print 'pp3e mod:', root['pp3e'].modtime
root['pp3e'].updateBookmark('PP3E', 'www.rmi.net/~lutz/about-pp3e.html')

# this updates too: attr changed here
ora = root['ora']
print 'ora hits:', ora.hits
ora.hits += 1

# commit changes made
import transaction
transaction.commit()
storage.close()
