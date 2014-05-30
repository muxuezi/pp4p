"list file tree with os.walk"

import sys, os

def lister(root):                                           # for a root dir
    for (thisdir, subshere, fileshere) in os.walk(root):    # generate dirs in tree
        print('[' + thisdir + ']')
        for fname in fileshere:                             # print files in this dir
            path = os.path.join(thisdir, fname)             # add dir name prefix
            print(path)

if __name__ == '__main__':
    lister(sys.argv[1])                                     # dir name in cmdline
