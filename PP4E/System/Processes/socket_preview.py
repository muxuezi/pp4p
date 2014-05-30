"""
sockets for cross-task communication: start threads to communicate over sockets;
independent programs can too, because sockets are system-wide, much like fifos;
see the GUI and Internet parts of the book for more realistic socket use cases;
some socket servers may also need to talk to clients in threads or processes;
sockets pass byte strings, but can be pickled objects or encoded Unicode text;
caveat: prints in threads may need to be synchronized if their output overlaps;
"""

from socket import socket, AF_INET, SOCK_STREAM     # portable socket api

port = 50008                 # port number identifies socket on machine
host = 'localhost'           # server and client run on same local machine here

def server():
    sock = socket(AF_INET, SOCK_STREAM)         # ip addresses tcp connection
    sock.bind(('', port))                       # bind to port on this machine
    sock.listen(5)                              # allow up to 5 pending clients
    while True:
        conn, addr = sock.accept()              # wait for client to connect
        data = conn.recv(1024)                  # read bytes data from this client
        reply = 'server got: [%s]' % data       # conn is a new connected socket
        conn.send(reply.encode())               # send bytes reply back to client

def client(name):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))                  # connect to a socket port
    sock.send(name.encode())                    # send bytes data to listener
    reply = sock.recv(1024)                     # receive bytes data from listener
    sock.close()                                # up to 1024 bytes in message
    print('client got: [%s]' % reply)

if __name__ == '__main__':
    from threading import Thread
    sthread = Thread(target=server)
    sthread.daemon = True                       # don't wait for server thread
    sthread.start()                             # do wait for children to exit
    for i in range(5): 
         Thread(target=client, args=('client%s' % i,)).start()

