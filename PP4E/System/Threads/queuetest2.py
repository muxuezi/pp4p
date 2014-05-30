"same as queuetest.py, by queue object pass in as argument, not global"


numconsumers = 2                  # how many consumers to start
numproducers = 4                  # how many producers to start
nummessages  = 4                  # messages per producer to put

import _thread as thread, queue, time
safeprint = thread.allocate_lock()    # else prints may overlap
dataQueue = queue.Queue()             # shared global, infinite size

def producer(idnum, dataqueue):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataqueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum, dataqueue):
    while True:
        time.sleep(0.1)
        try:
            data = dataqueue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread.start_new_thread(consumer, (i, dataQueue))
    for i in range(numproducers):
        thread.start_new_thread(producer, (i, dataQueue))
    time.sleep(((numproducers-1) * nummessages) + 1)
    print('Main thread exit.')
