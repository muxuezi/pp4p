"""
###########################################################################################
Same as fork-server.py, but use multiprocessing instead of os.fork;
this works on Cygwin, and probably works on other Unix-likes, because 
multiprocessing forks and descriptors are inherited, but it fails on 
Windows (sockets do not pickle correctly as arguments to the Process target), 
and would be very slow in any event (starting a new Python interpreter versus
starting an in-process thread);  I get this in 3.1 on Windows 7:

Parent: 4768
Server connected by ('127.0.0.1', 58061) at Fri Apr 23 14:48:01 2010
Child: 8688
Process Process-1:
Traceback (most recent call last):
  File "C:\Python31\lib\multiprocessing\process.py", line 233, in _bootstr
    self.run()
  File "C:\Python31\lib\multiprocessing\process.py", line 88, in run
    self._target(*self._args, **self._kwargs)
  File "C:\...\PP4E\Internet\Sockets\multi-server.py", line 22, in handleClient
    data = connection.recv(1024)             # till eof when socket closed
socket.error: [Errno 10038] An operation was attempted on something that is not a socket
###########################################################################################
"""

import os, time, sys
from multiprocessing import Process
from socket import *                      # get socket constructor and constants
myHost = ''                               # server machine, '' means local host
myPort = 50007                            # listen on a non-reserved port number

def now():                                       # current time on server
    return time.ctime(time.time())

def handleClient(connection):
    print('Child:', os.getpid())                 # child process: reply, exit
    time.sleep(5)                                # simulate a blocking activity
    while True:                                  # read, write a client socket
        data = connection.recv(1024)             # till eof when socket closed
        if not data: break
        reply = 'Echo=>%s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()

def dispatcher():                                # listen until process killed
    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to process for service
        print('Server connected by', address, end=' ')
        print('at', now())
        Process(target=handleClient, args=(connection,)).start()

if __name__ == '__main__':
    print('Parent:', os.getpid())
    sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
    sockobj.bind((myHost, myPort))                   # bind it to server port number
    sockobj.listen(5)                                # allow 5 pending connects
    dispatcher()
