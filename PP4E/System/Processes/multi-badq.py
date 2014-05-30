### these both fail: can't put bound method on Pipe or Queue!


class Spam:
   def action(self): print(99)


from multiprocessing import Process, Pipe

def sender(pipe):
    pipe.send(Spam().action)
    pipe.close() 

if __name__ == '__main__':
    (parentEnd, childEnd) = Pipe()                   
    Process(target=sender, args=(childEnd,)).start()        # spawn child with pipe
    print('parent got:', parentEnd.recv())                  # receive from child
    print('parent exit')



"""
import os, time, queue
from multiprocessing import Process, Queue           # process-safe shared queue
                                                     # queue is a pipe + locks/semas
class Counter(Process):
    def __init__(self, queue):                       # retain state for us in run
        self.post = queue
        Process.__init__(self)

    def run(self):                                   # run in newprocess on start()
        for i in range(3):
            time.sleep(1)
            self.post.put(Spam().action)             # stdout file is shared by all
        print('child exit')

if __name__ == '__main__':
    print('start', os.getpid())
    post = Queue()
    p = Counter(post)       
    p.start()
    while True:                                 # parent consumes data on queue                         
        time.sleep(0.5)                         # this is essentially like a GUI,
        try:                                    # though GUIs often use threads
            data = post.get(block=False)
        except queue.Empty:
            print('no data...')
        else:
            print('posted:', data)
            break
    p.join()
    print('finish', os.getpid(), p.exitcode)    # exitcode is child exit status
"""