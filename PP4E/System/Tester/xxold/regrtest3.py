# test driver
import glob, sys, os
if len(sys.argv) > 1:
    testdir = sys.argv[1]
else:
    testdir = 'scripts'

for py in glob.glob(os.path.join(testdir, '*.py')):

    #pipe = os.popen(py)
    #output = pipe.read()

    argsname = py + '.args'
    if os.path.exists(argsname):
        args = open(argsname).read()
    else:
        args = ''
        
    (stdin, stdout, stderr) = os.popen3(sys.executable + ' ' + py + ' ' + args)
    output = stdout.read()
    error  = stderr.read()
    if error:
        print 'Error:', py, output, error
        output = output + error

    outname = py + '.out'
    if not os.path.exists(outname):
        open(outname, 'w').write(output)
        print 'Generated:', outname
    else:
        prioroutput = open(outname).read()
        if output == prioroutput:
            print 'Passed:', py
        else:
            print 'FAILED:', py
