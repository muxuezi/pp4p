"""
FAILS! -- tkinter doesn't support parallel GUI updates in threads
"""

import _thread, threading
from tkinter import *
demoModules = ['demoDlg', 'demoRadio', 'demoCheck', 'demoScale']

def makePopups(modnames):
    demoObjects = []
    for modname in modnames:
        module = __import__(modname)          # import by name string
        _thread.start_new_thread(build, (module,))
        #threading.Thread(target=build, args=(module,)).start()
        #build(module)
    return demoObjects

def build(module):
    window = Toplevel()                   # make a new window
    demo   = module.Demo(window)          # parent is the new window
    window.title(module.__name__)
    #demoObjects.append(demo)

def allstates(demoObjects):
    for obj in demoObjects:
        if hasattr(obj, 'report'):
            print(obj.__module__, end=' ')
            obj.report()

root = Tk()                                   # make explicit root first
root.title('Popups')
demos = makePopups(demoModules)
Label(root, text='Multiple Toplevel window demo', bg='white').pack()
Button(root, text='States', command=lambda: allstates(demos)).pack(fill=X)
root.mainloop()
