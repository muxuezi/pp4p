# same but try thread for read/write loop to avoid blocking: not safe!

from tkinter import *
from PP4E.Gui.Tools.guiStreams import redirectedGuiShellCmd

#def launch():
#    redirectedGuiShellCmd('python -u pipe-nongui.py')

def launch():
    import _thread
    print('starting thread')
    _thread.start_new_thread(redirectedGuiShellCmd, ('python -u pipe-nongui.py',))

window = Tk()
Button(window, text='GO!', command=launch).pack()
window.mainloop()
