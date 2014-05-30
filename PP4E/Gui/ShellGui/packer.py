# pack text files into a single file with separator lines (simple archive)

import sys, glob
marker = ':' * 20 + 'textpak=>'      # hopefully unique separator

def pack(ofile, ifiles):
    output = open(ofile, 'w')
    for name in ifiles:
        print('packing:', name)
        input = open(name, 'r').read()        # open the next input file
        if input[-1] != '\n': input += '\n'   # make sure it has endline
        output.write(marker + name + '\n')    # write a separator line
        output.write(input)                   # and write the file's contents

if __name__ == '__main__':
    ifiles = []
    for patt in sys.argv[2:]:
        ifiles += glob.glob(patt)             # not globbed auto on Windows
    pack(sys.argv[1], ifiles)                 # pack files listed on cmdline
