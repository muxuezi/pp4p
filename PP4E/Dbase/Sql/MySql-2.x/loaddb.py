###############################################################################
# like loaddb1, but insert more than one row at once, and reusable funtion
# command-line usage: loaddb.py dbname? datafile? (tablename is implied)
###############################################################################

tablename = 'people'   # generalize me

def login(host='localhost', user='root', passwd='python', db=None):
    import MySQLdb
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd)
    curs = conn.cursor()
    if db: curs.execute('use ' + db)
    return conn, curs
    
def loaddb(cursor, table, datafile='data.txt', conn=None):
    file = open(datafile)                            # x,x,x\nx,x,x\n
    rows = [line.split(',') for line in file]        # [ [x,x,x], [x,x,x] ]
    rows = [str(tuple(rec)) for rec in rows]         # [ "(x,x,x)", "(x,x,x)" ]
    rows = ', '.join(rows)                           # "(x,x,x), (x,x,x)"
    curs.execute('insert ' + table + ' values ' + rows)
    print curs.rowcount, 'rows loaded'
    if conn: conn.commit()    

if __name__ == '__main__':
    import sys
    database, datafile = 'peopledb', 'data.txt'
    if len(sys.argv) > 1: database = sys.argv[1]
    if len(sys.argv) > 2: datafile = sys.argv[2] 
    conn, curs = login(db=database)
    loaddb(curs, tablename, datafile, conn)
