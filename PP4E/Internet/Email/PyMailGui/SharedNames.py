"""
##############################################################################
objects shared by all window classes and main file: program-wide globals
##############################################################################
"""

# python 3.3+ hack (formataddr change)
import py33patch

# used in all window, icon titles
appname  = 'PyMailGUI 3.0'

# used for list save, open, delete; also for sent messages file
saveMailSeparator = 'PyMailGUI' + ('-'*60) + 'PyMailGUI\n'

# currently viewed mail save files; also for sent-mail file
openSaveFiles = {}                     # 1 window per file,{name:win}

# standard library services
import sys, os, email.utils, email.message, webbrowser, mimetypes
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.filedialog   import SaveAs, Open, Directory
from tkinter.messagebox   import showinfo, showerror, askyesno

# reuse book examples
from PP4E.Gui.Tools      import windows      # window border, exit protocols
from PP4E.Gui.Tools      import threadtools  # thread callback queue checker
from PP4E.Internet.Email import mailtools    # load,send,parse,build utilities
from PP4E.Gui.TextEditor import textEditor   # component and pop up

# modules defined here
import mailconfig                            # user params: servers, fonts, etc.
import popuputil                             # help, busy, passwd pop-up windows
import wraplines                             # wrap long message lines
import messagecache                          # remember already loaded mail
import html2text                             # simplistic html->plaintext extract
import PyMailGuiHelp                         # user documentation

def printStack(exc_info):
    """
    debugging: show exception and stack traceback on stdout;
    3.0: change to print stack trace to a real log file if print
    to sys.stdout fails: it does when launched from another program
    on Windows;  without this workaround, PMailGUI aborts and exits
    altogether, as this is called from the main thread on spawned 
    thread failures;  likely a Python 3.1 bug: it doesn't occur in 
    2.5 or 2.6, and the traceback object works fine if print to file;
    oddly, the print() calls here work (but go nowhere) if spawned;
    """
    print(exc_info[0])
    print(exc_info[1])
    import traceback
    try:
        traceback.print_tb(exc_info[2], file=sys.stdout)   # ok unless spawned!
    except:
        log = open('_pymailerrlog.txt', 'a')               # use a real file 
        log.write('-'*80)                                  # else gui may exit
        traceback.print_tb(exc_info[2], file=log)          # in 3.X, not 2.5/6

# thread busy counters for threads run by this GUI
# sendingBusy shared by all send windows, used by main window quit

loadingHdrsBusy = threadtools.ThreadCounter()   # only 1
deletingBusy    = threadtools.ThreadCounter()   # only 1
loadingMsgsBusy = threadtools.ThreadCounter()   # poss many
sendingBusy     = threadtools.ThreadCounter()   # poss many
