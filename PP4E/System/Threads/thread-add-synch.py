"prints 200 each time, because shared resource access synchronized"

import threading, time
count = 0

def adder(addlock):                 # shared lock object passed in
    global count
    with addlock: 
        count = count + 1           # auto acquire/release around stmt 
    time.sleep(0.5)
    with addlock:
        count = count + 1           # only 1 thread updating at once

addlock = threading.Lock()
threads = []
for i in range(100):
    thread = threading.Thread(target=adder, args=(addlock,))
    thread.start()
    threads.append(thread)

for thread in threads: thread.join()
print(count)