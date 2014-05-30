"Remove all .pyc bytecode files in a tree (visitor version)"

import sys, os
from visitor import FileVisitor

class CleanPyc(FileVisitor):
    def __init__(self, trace=0):
        FileVisitor.__init__(self, context=0, trace=trace)

    def visitfile(self, filepath):
        FileVisitor.visitfile(self, filepath)
        if filepath.endswith('.pyc'):
            print(filepath) 
            #os.remove(filepath)
            self.context += 1

if __name__ == '__main__':
    walker = CleanPyc()
    walker.run(sys.argv[1] if len(sys.argv) > 1 else '.')
    print('Visited %d files and %d dirs' % (walker.fcount, walker.dcount))
    print('Removed %d files' % walker.context)