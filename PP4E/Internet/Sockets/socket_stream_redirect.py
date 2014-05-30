"""
###############################################################################
Tools for connecting standard streams of non-GUI programs to sockets that 
a GUI (or other) program can use to interact with the non-GUI program.
###############################################################################
"""

import sys
from socket import *
port = 50008            # pass in different port if multiple dialogs on machine
host = 'localhost'      # pass in different host to connect to remote listeners                 

def initListenerSocket(port=port):
    """
    initialize connected socket for callers that listen in server mode
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))                     # listen on this port number
    sock.listen(5)                            # set pending queue length
    conn, addr = sock.accept()                # wait for client to connect
    return conn                               # return connected socket

def redirectOut(port=port, host=host):  
    """
    connect caller's standard output stream to a socket for GUI to listen 
    start caller after listener started, else connect fails before accept
    """
    sock = socket(AF_INET, SOCK_STREAM)  
    sock.connect((host, port))                # caller operates in client mode
    file = sock.makefile('w')                 # file interface: text, buffered
    sys.stdout = file                         # make prints go to sock.send
    return sock                               # if caller needs to access it raw

def redirectIn(port=port, host=host):
    """
    connect caller's standard input stream to a socket for GUI to provide 
    """
    sock = socket(AF_INET, SOCK_STREAM)  
    sock.connect((host, port))
    file = sock.makefile('r')                 # file interface wrapper
    sys.stdin = file                          # make input come from sock.recv
    return sock                               # return value can be ignored

def redirectBothAsClient(port=port, host=host):
    """
    connect caller's standard input and output stream to same socket
    in this mode, caller is client to a server: sends msg, receives reply
    """
    sock = socket(AF_INET, SOCK_STREAM)  
    sock.connect((host, port))                # or open in 'rw' mode
    ofile = sock.makefile('w')                # file interface: text, buffered
    ifile = sock.makefile('r')                # two file objects wrap same socket
    sys.stdout = ofile                        # make prints go to sock.send
    sys.stdin  = ifile                        # make input come from sock.recv
    return sock

def redirectBothAsServer(port=port, host=host):
    """
    connect caller's standard input and output stream to same socket
    in this mode, caller is server to a client: receives msg, send reply
    """
    sock = socket(AF_INET, SOCK_STREAM)  
    sock.bind((host, port))                   # caller is listener here
    sock.listen(5)
    conn, addr = sock.accept()
    ofile = conn.makefile('w')                # file interface wrapper
    ifile = conn.makefile('r')                # two file objects wrap same socket
    sys.stdout = ofile                        # make prints go to sock.send
    sys.stdin  = ifile                        # make input come from sock.recv
    return conn
