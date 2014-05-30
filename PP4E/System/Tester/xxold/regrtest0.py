#!/usr/local/bin/python
import os, sys, time                        # get system, python services
from glob import glob                       # filename expansion

print 'RegTest start.'
print 'user:', os.environ['USER']           # environment variables
print 'path:', os.getcwd()                  # current directory
print 'time:', time.asctime(), '\n'
program = sys.argv[1]                       # two command-line args
testdir = sys.argv[2]

for test in glob(testdir + '/*.in'):        # for all matching input files
    if not os.path.exists('%s.out' % test):
        # no prior results
        os.system('%s < %s > %s.out 2>&1' % (program, test, test))
        print 'GENERATED:', test
    else:
        # backup, run, compare
        os.rename(test + '.out', test + '.out.bkp')
        os.system('%s < %s > %s.out 2>&1' % (program, test, test))
        os.system('diff %s.out %s.out.bkp > %s.diffs' % ((test,)*3) )
        if os.path.getsize(test + '.diffs') == 0:
            print 'PASSED:', test
            os.remove(test + '.diffs')
        else:
            print 'FAILED:', test, '(see %s.diffs)' % test

print 'RegTest done:', time.asctime()
