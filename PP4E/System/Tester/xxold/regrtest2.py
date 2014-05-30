import os, sys, glob
testdir = sys.argv[1]
forcegen = len(sys.argv) > 2

testpatt  = os.path.join(testdir, 'tests', '*.py')
testfiles = glob.glob(testpatt)
testfiles.sort()
for test in testfiles:
    infile = os.path.basename(test).replace('.py', '.in')
    inpath = os.path.join(testdir, 'inputs', infile)

    outfile = os.path.basename(test).replace('.py', '.out')
    outpath = os.path.join(testdir, 'outputs', outfile)

    argfile = os.path.basename(test).replace('.py', '.arg')
    argpath = os.path.join(testdir, 'args', argfile)

    pypath = sys.executable
    arglist = open(argpath).readline()
    (stdin, stdout) = os.popen2('%s %s %s' % (pypath, test, arglist))
    stdin.write(open(inpath).read())
    stdin.close()
    output = stdout.read()

    if not os.path.exists(outpath) or forcegen:
        print 'generating:', outpath
        open(outpath, 'w').write(output)
    else:
        oldout = open(outpath).read()
        if oldout == output:
            print 'passed:', test
        else:
            print 'FAILED:', test
