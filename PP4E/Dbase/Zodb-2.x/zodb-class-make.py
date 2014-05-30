#############################################################################
# define persistent class, store instances in a zodb database;
# import, call addobjects elsewhere: pickled class cannot be in __main__
#############################################################################

import time
mydbfile = 'data/class.fs'                         # where database is stored
from persistent import Persistent

class BookMark(Persistent):                        # inherit zodb features
    def __init__(self, title, url):
        self.hits = 0
        self.updateBookmark(self, url)
    def updateBookmark(self, title, url):
        self.title = title                         # change attrs updates db
        self.url = url                             # no need to reassign to key
        self.modtime = time.asctime()

def connectdb(dbfile):
    from ZODB import FileStorage, DB
    storage = FileStorage.FileStorage(dbfile)      # automate connect protocol
    db = DB(storage)                               # caller must still commit
    connection = db.open()
    root = connection.root()
    return root, storage

def addobjects():
    root, storage = connectdb(mydbfile)
    root['ora']  = BookMark('Oreilly', 'http://www.oreilly.com')
    root['pp3e'] = BookMark('PP3E',    'http://www.rmi.net/~lutz/about-pp.html')
    import transaction
    transaction.commit()
    storage.close()
