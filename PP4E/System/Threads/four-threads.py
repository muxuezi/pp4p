"""
four different ways to run an action in a thread; all print 4294967296,
but prints should be synchronized with a mutex here to avoid overlap
"""

import threading, _thread
def action(i): 
    print(i ** 32)

# subclass with state
class Mythread(threading.Thread):
    def __init__(self, i):
        self.i = i
        threading.Thread.__init__(self)
    def run(self):                                        # redefine run for action
        print(self.i ** 32)
Mythread(2).start()                                       # start invokes run()

# pass action in
thread = threading.Thread(target=(lambda: action(2)))     # run invokes target
thread.start()

# same but no lambda wrapper for state
threading.Thread(target=action, args=(2,)).start()        # callable plus its args

# basic thread module
_thread.start_new_thread(action, (2,))                    # all-function interface
