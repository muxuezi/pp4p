###############################################################################
# convert list of row tuples to list of row dicts with field name keys
# this is not a command-line utility: hard-coded self-test if run
###############################################################################

def makedicts(cursor, query, params=()):
    cursor.execute(query, params)
    colnames = [desc[0] for desc in cursor.description]
    rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    return rowdicts

if __name__ == '__main__':   # self test
    import MySQLdb
    conn = MySQLdb.connect(host='localhost', user='root', passwd='python')
    cursor = conn.cursor()
    cursor.execute('use peopledb')
    query  = 'select name, pay from people where pay < %s'
    lowpay = makedicts(cursor, query, [70000])
    for rec in lowpay: print rec   
