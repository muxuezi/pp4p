"""
FAILS! -- tkinter doesn't support parallel GUI updates in threads
"""

import _thread, threading
from tkinter import *
from quitter import Quitter
demoModules = ['demoDlg', 'demoCheck', 'demoRadio', 'demoScale']
parts = []

def addComponents(root):
    for demo in demoModules:
        module = __import__(demo)
        _thread.start_new_thread(build, (module,))
        #threading.Thread(target=build, args=(module,)).start()
        #build(module)

def build(module):
        #module = __import__(demo)                      # this has no effect
        part = module.Demo(root)                        # attach an instance
        part.config(bd=2, relief=GROOVE)                # or pass configs to Demo()
        part.pack(side=LEFT, expand=YES, fill=BOTH)     # grow, stretch with window
        parts.append(part)                              # change list in-place

def dumpState():
    for part in parts:                                  # run demo report if any
        print(part.__module__ + ':', end=' ')
        if hasattr(part, 'report'):
           part.report()
        else:
           print('none')

root = Tk()                                             # make explicit root first
root.title('Frames')
Label(root, text='Multiple Frame demo', bg='white').pack()
Button(root, text='States', command=dumpState).pack(fill=X)
Quitter(root).pack(fill=X)
addComponents(root)
root.mainloop()
