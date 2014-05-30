 ################################################################################
# load table from comma-delimited text file; equivalent to executing this sql:
# "load data local infile 'data.txt' into table people fields terminated by ','"
################################################################################

import MySQLdb
conn = MySQLdb.connect(host='localhost', user='root', passwd='python')
curs = conn.cursor()
curs.execute('use peopledb')

file = open('data.txt')
rows = [line.split(',') for line in file]
for rec in rows:
    curs.execute('insert people values (%s, %s, %s)', rec)

conn.commit()       # commit changes now, if db supports transactions
conn.close()        # close, __del__ call rollback if changes not commited yet
