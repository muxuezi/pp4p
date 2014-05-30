##########################################################
# view the person ZODB database in PyForm's FormGui;
# FileDB maps indexing to db root, close does commit;
# caveat 1: FormGui doesn't yet allow mixed class types;
# caveat 2: FormGui has no way to call class methods;
# caveat 3: Persistent subclasses don't allow __class__
# to be set: must have defaults for all __init__ args;
# Person here works only if always defined in __main__;
##########################################################

import sys
filename = 'data/people-simple.fs'
from zodbtools import FileDB
from PP3E.Dbase.TableBrowser.formgui   import FormGui
from PP3E.Dbase.TableBrowser.formtable import Table, InstanceRecord

class Person: pass
initrecs = {'bob': dict(name='bob', job='devel', pay=30),
            'sue': dict(name='sue', job='music', pay=40)}
            
dbtable = Table(FileDB(filename), InstanceRecord(Person))
if len(sys.argv) > 1:
    for key in dbtable.keys():
        del dbtable[key]                 # "viewzodb.py -" inits db
    dbtable.storeItems(initrecs)         # "viewzodb.py" browses db
    
FormGui(dbtable).mainloop()
dbtable.printItems()
dbtable.close()
