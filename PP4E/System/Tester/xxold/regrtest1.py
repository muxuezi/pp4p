import os, sys, glob
testdir   = 'Scripts'
outputdir = 'Outputs'

pypatt = os.path.join(testdir, '*.py')
print pypatt
for pyfile in glob.glob(pypatt):
    outname = os.path.join(outputdir, os.path.basename(pyfile) + '.out')
    output  = os.popen('%s %s' % (sys.executable, pyfile)).read()
    if not os.path.exists(outname):
        print 'Generating', outname
        open(outname, 'w').write(output)
    else:
        oldout = open(outname).read()
        if output != oldout:
            print 'FAILED', pyfile
        else:
            print 'passed', pyfile
print 'Finished.'