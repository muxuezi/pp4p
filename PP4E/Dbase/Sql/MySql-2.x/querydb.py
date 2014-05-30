###############################################################################
# run a query string, display formatted result table
# example: querydb.py testdb "select name, job from people where pay > 50000"
###############################################################################

import sys
database, query = 'peopledb', 'select * from people'
if len(sys.argv) > 1: database = sys.argv[1]
if len(sys.argv) > 2: query = sys.argv[2] 

from makedicts import makedicts
from dumpdb    import showformat
from loaddb    import login

conn, curs = login(db=database)
rows = makedicts(curs, query)
showformat(rows)
