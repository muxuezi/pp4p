###############################################################################
# display table contents as raw tuples, or formatted with field names
# command-line usage: dumpdb.py dbname? [-] (dash for formatted display)
###############################################################################

def showformat(recs, sept=('-' * 40)):
    print len(recs), 'records'
    print sept
    for rec in recs:
        maxkey = max(len(key) for key in rec)                # max key len
        for key in rec:                                      # or: \t align
            print '%-*s => %s' % (maxkey, key, rec[key])     # -ljust, *len
        print sept                                     

def dumpdb(cursor, table, format=True):
    if not format:
        cursor.execute('select * from ' + table)
        while True:
            rec = cursor.fetchone()
            if not rec: break
            print rec
    else:
        from makedicts import makedicts
        recs = makedicts(cursor, 'select * from ' + table)
        showformat(recs)

if __name__ == '__main__':
    import sys
    dbname, format = 'peopledb', False
    cmdargs = sys.argv[1:]
    if '-' in cmdargs:                     # format if '-' in cmdline args
        format = True                      # dbname if other cmdline arg
        cmdargs.remove('-')
    if cmdargs: 
        dbname = cmdargs[0]
        
    from loaddb import login
    conn, curs = login(db=dbname)
    dumpdb(curs, 'people', format)
