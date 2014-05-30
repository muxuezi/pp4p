"same as queuetest2.py, but uses threading, not _threads"


numconsumers = 2                  # how many consumers to start
numproducers = 4                  # how many producers to start
nummessages  = 4                  # messages per producer to put

import threading, queue, time
safeprint = threading.Lock()          # else prints may overlap
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
        thread = threading.Thread(target=consumer, args=(i, dataQueue))
        thread.daemon = True  # else cannot exit!
        thread.start()

    waitfor = []
    for i in range(numproducers):
        thread = threading.Thread(target=producer, args=(i, dataQueue))
        waitfor.append(thread)
        thread.start()

    for thread in waitfor: thread.join()    # or time.sleep() long enough here
    print('Main thread exit.')
