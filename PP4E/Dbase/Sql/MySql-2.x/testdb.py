from MySQLdb import Connect
conn = Connect(host='localhost', user='root', passwd='python')
curs = conn.cursor()
try:
    curs.execute('drop database testpeopledb')
except:
    pass  # did not exist

curs.execute('create database testpeopledb')
curs.execute('use testpeopledb')
curs.execute('create table people (name char(30), job char(10), pay int(4))')

curs.execute('insert people values (%s, %s, %s)', ('Bob', 'dev', 50000))
curs.execute('insert people values (%s, %s, %s)', ('Sue', 'dev', 60000))

curs.execute('select * from people')
for row in curs.fetchall():
	print row

curs.execute('select * from people')
colnames = [desc[0] for desc in curs.description]
while True:
    print '-' * 30
    row = curs.fetchone()
    if not row: break
    for (name, value) in zip(colnames, row):
        print '%s => %s' % (name, value)

conn.commit()   # save inserted records
