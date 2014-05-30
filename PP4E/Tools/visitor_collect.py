"""
Use: "python ...\Tools\visitor_collect.py searchstring rootdir".
CollectVisitor simply collects a list of all files containing a search
string, for display or later processing (e.g., replacement, auto-editing);
pass in a test filename extensions list to constructor to override the
default in SearchVisitor; this is roughy like find+grep for text exts;
"""

import sys
from visitor import SearchVisitor

class CollectVisitor(SearchVisitor):
    """
    collect names of files containing a string;
    run this and then fetch its obj.matches list
    """
    def __init__(self, searchstr, testexts=None, trace=1):
        self.matches = []
        if testexts != None: self.testexts = testexts
        SearchVisitor.__init__(self, searchstr, trace)
    def visitmatch(self, fname, text):
        self.matches.append(fname)

if __name__  == '__main__':
    visitor = CollectVisitor(sys.argv[1])
    visitor.run(startDir=sys.argv[2])
    matches = visitor.matches
    print('Found', len(matches), 'files:')
    for fname in matches: print(fname)
