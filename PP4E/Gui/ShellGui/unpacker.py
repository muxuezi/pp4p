# unpack files created by packer.py (simple textfile archive)

import sys
from packer import marker             # use common separator key
mlen = len(marker)                    # filenames after markers

def unpack(ifile, prefix='new-'):
    for line in open(ifile):                # for all input lines
        if line[:mlen] != marker:
            output.write(line)              # write real lines
        else:
            name = prefix + line[mlen:-1]   # or make new output
            print('creating:', name)
            output = open(name, 'w')

if __name__ == '__main__': unpack(sys.argv[1])
