# test exit status: good exit code
import sys
print('starting', sys.argv[0])
sys.exit(int(sys.argv[1]))            # zero

