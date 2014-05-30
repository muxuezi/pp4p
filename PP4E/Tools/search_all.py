"""
################################################################################
Use: "python ...\Tools\search_all.py dir string".
Search all files at and below a named directory for a string; uses the
os.walk interface, rather than doing a find.find to collect names first;
similar to calling visitfile for each find.find result for "*" pattern;
################################################################################
"""

import os, sys
listonly = False
textexts = ['.py', '.pyw', '.txt', '.c', '.h']             # ignore binary files

def searcher(startdir, searchkey):
    global fcount, vcount
    fcount = vcount = 0
    for (thisDir, dirsHere, filesHere) in os.walk(startdir):
        for fname in filesHere:                            # do non-dir files here
            fpath = os.path.join(thisDir, fname)           # fnames have no dirpath
            visitfile(fpath, searchkey)

def visitfile(fpath, searchkey):                           # for each non-dir file
    global fcount, vcount                                  # search for string
    print(vcount+1, '=>', fpath)                           # skip protected files
    try:
        if not listonly:
            if os.path.splitext(fpath)[1] not in textexts:
                print('Skipping', fpath)
            elif searchkey in open(fpath).read():
                input('%s has %s' % (fpath, searchkey))
                fcount += 1
    except:
        print('Failed:', fpath, sys.exc_info()[0])
    vcount += 1

if __name__ == '__main__':
    searcher(sys.argv[1], sys.argv[2])
    print('Found in %d files, visited %d' % (fcount, vcount))
