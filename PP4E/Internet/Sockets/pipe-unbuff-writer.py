# output line buffered (unbuffered) if stdout is a terminal, buffered by default for
# other devices: use -u or sys.stdout.flush() to avoid delayed output on pipe/socket

import time, sys
for i in range(5):
    print(time.asctime())                 # print transfers per stream buffering
    sys.stdout.write('spam\n')            # ditto for direct stream file access
    time.sleep(2)                         # unles sys.stdout reset to other file
