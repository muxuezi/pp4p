"""
any callable can be run in a thread, since all live in same process;
add locks to synchronize prints if needed to avoid overlaps or output
dupication (see later in the chapter); all 3 threads print 4294967296
"""

import _thread, time

def action(i):                                       # function run in threads
    print(i ** 32)

class Power:
    def __init__(self, i):
        self.i = i
    def action(self):                                # bound method run in threads
        print(self.i ** 32)

_thread.start_new_thread(action, (2,))               # simple function

_thread.start_new_thread((lambda: action(2)), ())    # lambda function to defer

obj = Power(2)
_thread.start_new_thread(obj.action, ())             # bound method object

time.sleep(2)
print('Main thread exiting.')                        # don't exit too early
