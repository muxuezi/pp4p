# tests thread callback queue, but uses class bound methods for action and callbacks

import time
from threadtools import threadChecker, startThread
from tkinter.scrolledtext import ScrolledText

class MyGUI:
    def __init__(self, reps=3):
        self.reps = reps                        # uses default Tk root
        self.text = ScrolledText()              # save widget as state
        self.text.pack()
        threadChecker(self.text)                # start thread check loop
        self.text.bind('<Button-1>',            # 3.x need list for map, range ok
              lambda event: list(map(self.onEvent, range(6))) )
        
    def onEvent(self, i):                       # code that spawns thread
        myname = 'thread-%s' % i
        startThread(
            action     = self.threadaction,
            args       = (i, ),
            context    = (myname,),
            onExit     = self.threadexit,
            onFail     = self.threadfail,
            onProgress = self.threadprogress)

    # thread's main action
    def threadaction(self, id, progress):       # what the thread does
        for i in range(self.reps):              # access to object state here
            time.sleep(1)
            if progress: progress(i)            # progress callback: queued
        if id % 2 == 1: raise Exception         # odd numbered: fail

    # thread callbacks: dispatched off queue in main thread
    def threadexit(self, myname):
        self.text.insert('end', '%s\texit\n' % myname)
        self.text.see('end')

    def threadfail(self, exc_info, myname):     # have access to self state
        self.text.insert('end', '%s\tfail\t%s\n' % (myname, exc_info[0]))
        self.text.see('end')

    def threadprogress(self, count, myname):
        self.text.insert('end', '%s\tprog\t%s\n' % (myname, count))
        self.text.see('end')
        self.text.update()   # works here: run in main thread

if __name__ == '__main__': MyGUI().text.mainloop()
