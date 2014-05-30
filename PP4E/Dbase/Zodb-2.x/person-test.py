##############################################################################
# test persistence classes in person.py; this runs as __main__, so the
# classes cannot be defined in this file: class's module must be importable
# when obj fetched; can also test from interactive prompt: also is __main__
##############################################################################

from zodbtools import FileDB                     # extended db root 
from person import Person, Engineer              # application objects
filename = 'people.fs'                           # external storage

import sys
if len(sys.argv) == 1:                           # no args: create test records
    db = FileDB(filename)                        # db is root object
    db['bob'] = Person('bob', 'devel', 30)       # stores in db
    db['sue'] = Person('sue', 'music', 40)
    tom = Engineer('tom', 'devel', 60000)
    db['tom'] = tom
    db.close()                                   # close commits changes

else:                                            # arg: change tom, sue each run
    db = FileDB(filename)
    print db['bob'].name, db.keys()
    print db['sue']
    db['sue'].changeRate(db['sue'].rate + 10)    # updates db
    tom = db['tom']
    print tom
    tom.changeRate(tom.rate + 5000)              # updates db
    tom.name += '.spam'                          # updates db
    db.close()
