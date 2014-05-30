#!/usr/local/bin/python
"""
The following additional re patterns example from the 3rd Edition was 
cut from the 4th; it was converted to but not tested under Python 3.X.
See its description bolw the code.
"""

import sys, re, glob

help_string = """
Usage options.
interactive:  % pygrep1.py
"""

def getargs():
    if len(sys.argv) == 1:
        return input("patterns? >").split(), input("files? >")
    else:
        try:
            return sys.argv[1], sys.argv[2]
        except:
            print(help_string)
            sys.exit(1)

def compile_patterns(patterns):
    res = []
    for pattstr in patterns:
        try:
            res.append(re.compile(pattstr))           # make re patt object
        except:                                       # or use re.match
            print('pattern ignored:', pattstr)
    return res

def searcher(pattfile, srchfiles):
    patts = compile_patterns(pattfile)                  # compile for speed
    for file in glob.glob(srchfiles):                   # all matching files
        lineno = 1                                      # glob uses re too
        print('\n[%s]' % file)
        for line in open(file, 'r'):                    # all lines in file
            for patt in patts:
                if patt.search(line):                   # try all patterns
                    print('%04d)' % lineno, line, end=' ') # match if not None
                    break
            lineno += 1

if __name__ == '__main__':
    searcher(*getargs())                                # was apply(func, args)





"""
-----------------------------------------------------------------------------------
A File Pattern Search Utility
The next script searches for patterns in a set of files, much like the grep 
command-line program. We wrote file and directory searchers earlier in Chapter 6. 
Here, the file searches look for patterns rather than simple strings, as coded in
Example 19-8. The patterns are typed interactively, separated by a space, and the
files to be searched are specified by an input pattern for Python’s glob.glob 
filename expansion tool that we studied earlier.

Example 19-8 (PP4E\Lang\pygrep1.py)

Here’s what a typical run of this script looks like, scanning old versions of some 
of the source files in this chapter; it searches all Python files in the current 
directory for two different patterns, compiled for speed. Notice that files are 
named by a pattern too—Python’s glob module also uses re internally:

C:\...\PP4E\Lang> python pygrep1.py
patterns? >import.*string spam
files? >*.py

[cheader.py]

[finder2.py]
0002) import string, glob, os, sys

[patterns.py]
0048) mobj = patt.search(" # define  spam  1 + 2 + 3")

[pygrep1.py]

[rules.py]

[summer.py]
0002) import string

[__init__.py]
-----------------------------------------------------------------------------------
"""