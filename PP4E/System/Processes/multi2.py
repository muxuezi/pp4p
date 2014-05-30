"""
Use multiprocess anonymous pipes to communicate. Returns 2 connection
object representing ends of the pipe: objects are sent on one end and
received on the other, though pipes are bidirectional by default
"""

import os
from multiprocessing import Process, Pipe

def sender(pipe):
    """
    send object to parent on anonymous pipe
    """
    pipe.send(['spam'] +  [42, 'eggs'])
    pipe.close() 

def talker(pipe):
    """
    send and receive objects on a pipe
    """
    pipe.send(dict(name='Bob', spam=42))
    reply = pipe.recv()
    print('talker got:', reply)

if __name__ == '__main__':
    (parentEnd, childEnd) = Pipe()                   
    Process(target=sender, args=(childEnd,)).start()        # spawn child with pipe
    print('parent got:', parentEnd.recv())                  # receive from child
    parentEnd.close()                                       # or auto-closed on gc

    (parentEnd, childEnd) = Pipe()
    child = Process(target=talker, args=(childEnd,))
    child.start()
    print('parent got:', parentEnd.recv())                  # receieve from child
    parentEnd.send({x * 2 for x in 'spam'})                 # send to child
    child.join()                                            # wait for child exit
    print('parent exit')
