"""
named pipes; os.mkfifo is not available on Windows (without Cygwin); 
there is no reason to fork here, since fifo file pipes are external 
to processes--shared fds in parent/child processes are irrelevent;
"""

import os, time, sys
fifoname = '/tmp/pipefifo'                       # must open same name

def child():
    pipeout = os.open(fifoname, os.O_WRONLY)     # open fifo pipe file as fd
    zzz = 0
    while True:
        time.sleep(zzz)
        msg = ('Spam %03d\n' % zzz).encode()     # binary as opened here
        os.write(pipeout, msg)
        zzz = (zzz+1) % 5

def parent():
    pipein = open(fifoname, 'r')                 # open fifo as text file object
    while True:
        line = pipein.readline()[:-1]            # blocks until data sent
        print('Parent %d got "%s" at %s' % (os.getpid(), line, time.time()))

if __name__ == '__main__':
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)                      # create a named pipe file
    if len(sys.argv) == 1:
        parent()                                 # run as parent if no args
    else:                                        # else run as child process
        child()
