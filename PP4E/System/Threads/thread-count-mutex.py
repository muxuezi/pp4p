"""
synchronize access to stdout: because it is shared global,
thread outputs may be intermixed if not synchronized
"""

import _thread as thread, time

def counter(myId, count):                        # function run in threads
    for i in range(count):
        time.sleep(1)                            # simulate real work
        mutex.acquire()
        print('[%s] => %s' % (myId, i))          # print isn't interrupted now
        mutex.release()

mutex = thread.allocate_lock()                   # make a global lock object
for i in range(5):                               # spawn 5 threads
    thread.start_new_thread(counter, (i, 5))     # each thread loops 5 times

time.sleep(6)
print('Main thread exiting.')                    # don't exit too early
