# GUI reader side: like pipes-gui1, but make root window and mainloop explicit

from tkinter import *
from PP4E.Gui.Tools.guiStreams import redirectedGuiShellCmd

def launch():
    redirectedGuiShellCmd('python -u pipe-nongui.py')

window = Tk()
Button(window, text='GO!', command=launch).pack()
window.mainloop()
