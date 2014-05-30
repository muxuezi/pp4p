"""
##############################################################################
Start various examples; run me at start time to make them always available.
This file is meant for starting programs you actually wish to use; see 
PyDemos for starting Python/Tk demos and more details on program start 
options.  Windows usage note: this is a '.py' to show messages in a console 
window when run or clicked (including a 10 second pause to make sure it's 
visible while gadgets start if clicked).  To avoid Windows console pop up,
run with the 'pythonw' program (not 'python'), rename to '.pyw' suffix, 
mark with 'run minimized' window property, or spawn elsewhere (see PyDemos).
##############################################################################
"""

import sys, time, os, time
from tkinter import *
from launchmodes import PortableLauncher           # reuse program start class
from Gui.Tools.windows import MainWindow           # reuse window tools: icon, quit

def runImmediate(mytools):
    """
    launch gadget programs immediately
    """
    print('Starting Python/Tk gadgets...')         # msgs to stdout (poss temp)
    for (name, commandLine) in mytools:
        PortableLauncher(name, commandLine)()      # call now to start now
    print('One moment please...')
    if sys.platform[:3] == 'win':                  # windows: keep console 10 secs
        for i in range(10): 
            time.sleep(1); print('.' * 5 * (i+1))

def runLauncher(mytools):
    """
    pop up a simple launcher bar for later use
    """
    root = MainWindow('PyGadgets PP4E')            # or root = Tk() if prefer
    for (name, commandLine) in mytools:
        b = Button(root, text=name, fg='black', bg='beige', border=2,
                   command=PortableLauncher(name, commandLine))
        b.pack(side=LEFT, expand=YES, fill=BOTH)
    root.mainloop()

mytools = [
    ('PyEdit',   'Gui/TextEditor/textEditor.py'),
    ('PyCalc',   'Lang/Calculator/calculator.py'),
    ('PyPhoto',  'Gui/PIL/pyphoto1.py Gui/PIL/images'),
    ('PyMail',   'Internet/Email/PyMailGui/PyMailGui.py'),
    ('PyClock',  'Gui/Clock/clock.py -size 175 -bg white'
                          ' -picture Gui/gifs/pythonPowered.gif'),
    ('PyToe',    'Ai/TicTacToe/tictactoe.py'
                          ' -mode Minimax -fg white -bg navy'),
    ('PyWeb',    'LaunchBrowser.pyw'
                          ' -live index.html www.rmi.net/~lutz')]
                         #' -live PyInternetDemos.html localhost:80')]
                         #' -file')] # PyInternetDemos assumes local server started

if __name__ == '__main__':
    prestart, toolbar = True, False
    if prestart:
        runImmediate(mytools)
    if toolbar:
        runLauncher(mytools)
