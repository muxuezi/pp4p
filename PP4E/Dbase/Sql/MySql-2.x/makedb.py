###############################################################################
# physically delete and recreate db files in mysql's data\ directory
# usage: makedb.py dbname? (tablename is implied)
###############################################################################

import sys
dbname = (len(sys.argv) > 1 and sys.argv[1]) or 'peopledb'

if raw_input('Are you sure?') not in ('y', 'Y', 'yes'):
    sys.exit()

from loaddb import login
conn, curs = login(db=None)
try:
    curs.execute('drop database ' + dbname)
except:
    print 'database did not exist'

curs.execute('create database ' + dbname)        # also: 'drop table tablename'
curs.execute('use ' + dbname)
curs.execute('create table people (name char(30), job char(10), pay int(4))')
conn.commit()   # this seems optional
print 'made', dbname
