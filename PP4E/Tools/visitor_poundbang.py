"""
Change all "#!...python" source lines at the top of Unix scripts to
new line in all files in all dirs at and below a root; command line args
are the root (default='.'), new #! line text (default=changeToDefault), 
and any text to run list-only mode (default=no); 

could skip binary filename extensions explicitly, but try handler works;
changes all #! first lines that name python, which is more accurate than  
a simple visitor_replace.py; example usage -- convert all scripts in book
examples tree, list file to be changed in a tree, convert all to default:
C:\...\PP4E>python Tools\visitor_poundbang.py . #!\MyPy31\python > out.txt
C:\...\PP4E\Tools>python visitor_poundbang.py C:\temp\PP3E - - | more
C:\...\PP4E\Tools>python visitor_poundbang.py C:\temp\PP3E
"""

import sys
from visitor import FileVisitor                 # reuse the walker classes
changeToDefault = '#!\Python31\python.exe'      # used if no cmdline arg

class PoundBangFixer(FileVisitor):
    def __init__(self, changeTo=changeToDefault, listonly=False, trace=0):
        FileVisitor.__init__(self, trace=trace)
        self.changeTo = changeTo
        self.listOnly = listonly
        self.clist    = []

    def visitfile(self, fullname):
        FileVisitor.visitfile(self, fullname)
        try:
            lines = open(fullname, 'r').readlines()      # fails for binary files
        except UnicodeDecodeError:
            if self.trace > 0: print('Skipped non-text file:', fullname)
        else:
            if (len(lines) > 0            and
                lines[0].startswith('#!') and            # or lines[0][0:2] == '#!'
                'python' in lines[0]                     # or lines[0].find() != -1
                ):
                self.clist.append(fullname)
                if not self.listOnly:
                    lines[0] = self.changeTo + '\n'
                    open(fullname, 'w').writelines(lines)

if __name__ == '__main__':
    if input('Are you sure?') != 'y': sys.exit()
    rootdir  = sys.argv[1] if len(sys.argv) > 1 else '.'
    changeto = sys.argv[2] if len(sys.argv) > 2 else changeToDefault
    listonly = len(sys.argv) > 3
    walker   = PoundBangFixer(changeto, listonly)
    walker.run(rootdir)
    print('Visited %d files and %d dirs,' % (walker.fcount, walker.dcount), end=' ')
    print('found' if listonly else 'changed', len(walker.clist), 'files')
    for fname in walker.clist: print(fname)
