###############################################################################
# delete all rows in table, but don't drop the table or database it is in
# usage: cleardb.py dbname? (tablename is implied)
###############################################################################

import sys
if raw_input('Are you sure?') not in ('y', 'Y', 'yes'):
    sys.exit()
dbname = 'peopledb'                             # cleardb.py
if len(sys.argv) > 1: dbname = sys.argv[1]      # cleardb.py testdb

from loaddb import login
conn, curs = login(db=dbname)
curs.execute('delete from people')
conn.commit()                                   # else rows not really deleted
print curs.rowcount, 'records deleted'          # conn closed by its __del__
