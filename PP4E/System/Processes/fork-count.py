"""
fork basics: start 5 copies of this program running in parallel with
the original; each copy counts up to 5 on the same stdout stream--forks
copy process memory, including file descriptors; fork doesn't currently
work on Windows without Cygwin: use os.spawnv or multiprocessing on
Windows instead; spawnv is roughly like a fork+exec combination;
"""

import os, time

def counter(count):                                    # run in new process
    for i in range(count):
        time.sleep(1)                                  # simulate real work
        print('[%s] => %s' % (os.getpid(), i))

for i in range(5):
    pid = os.fork()
    if pid != 0:
        print('Process %d spawned' % pid)              # in parent: continue
    else:
        counter(5)                                     # else in child/new process
        os._exit(0)                                    # run function and exit

print('Main process exiting.')                         # parent need not wait
