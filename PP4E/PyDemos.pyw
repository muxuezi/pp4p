"""
################################################################################
PyDemos.pyw
Programming Python, 2nd, 3rd, and 4th Editions (PP4E), 2001--2006--2010

Version 2.1 (4E), April '10: updated to run under Python 3.X, and spawn
local web servers for web demos only on first demo button selection.

Version 2.0 (3E), March '06: add source-code file viewer buttons; add new
Demos (PyPhoto, PyMailGUI); spawn locally running web servers for the 
browser-based Demos; add window icons; and probably more I've forgotten.

Launch major Python+Tk GUI examples from the book, in a platform-neutral way.
This file also serves as an index to major program examples, though many book
examples aren't GUI-based, and so aren't listed here.  Also see:

- PyGadgets.py, a simpler script for starting programs in non-demo mode
  that you wish to use on a regular basis
- PyGadgets_bar.pyw, which creates a button bar for starting all PyGadgets
  programs on demand, not all at once
- Launcher.py for starting programs without environment settings--finds
  Python, sets PYTHONPATH, etc.
- Launch_*.pyw for starting PyDemos and PyGadgets with Launcher.py--run these
  for a quick look
- LaunchBrowser.pyw for running example web pages with an automatically
  located web browser
- README-PP4E.txt, for general examples information

Caveat: this program tries to start a locally running web server and web 
Browser automatically, for web-based demos,  but does not kill the server. 
4E: web servers are only started when a web demo button is first selected,
and display in command-prompt windows on Windows to make more explicit; 
this still does not detect already-running server or server exit, though.  
################################################################################
"""

import sys, time, os, glob, launchmodes
from tkinter import *

# -live loads root pages from server so CGIs run, -file loads local files
InternetMode = '-live'

################################################################################
# start building main GUI windows
################################################################################

from PP4E.Gui.Tools.windows import MainWindow    # a Tk with icon, title, quit
from PP4E.Gui.Tools.windows import PopupWindow   # same but Toplevel, diff quit
Root = MainWindow('PP4E Demos 2.1')

# build message window
Stat = PopupWindow('PP4E demo info')
Stat.protocol('WM_DELETE_WINDOW', lambda:0)      # ignore wm delete

Info = Label(Stat, text = 'Select demo',
             font=('courier', 20, 'italic'), padx=12, pady=12, bg='lightblue')
Info.pack(expand=YES, fill=BOTH)

################################################################################
# add launcher buttons with callback objects
################################################################################

from PP4E.Gui.TextEditor.textEditor import TextEditorMainPopup

# demo launcher class
class Launcher(launchmodes.PortableLauncher):    # use wrapped launcher class
    def announce(self, text):                    # customize to set GUI label
        Info.config(text=text)

def viewer(sources):
    for filename in sources:
        TextEditorMainPopup(Root, filename,      # as pop up in this process
                            loadEncode='utf-8')  # else PyEdit may ask each!

def demoButton(name, what, doit, code, launcher=Launcher):
    """
    add buttons that runs doit command-line, and open all files in code;
    doit button retains state in an object, code in an enclosing scope;
    """
    rowfrm = Frame(Root)
    rowfrm.pack(side=TOP, expand=YES, fill=BOTH)

    b = Button(rowfrm, bg='navy', fg='white', relief=RIDGE, border=4)
    b.config(text=name, width=20, command=launcher(what, doit))
    b.pack(side=LEFT, expand=YES, fill=BOTH)

    b = Button(rowfrm, bg='beige', fg='navy')
    b.config(text='code', command=(lambda: viewer(code)))
    b.pack(side=LEFT, fill=BOTH)

# some imported module source files could be determined
# but we can't know where to stop on the import chains

################################################################################
# tkinter GUI demos - some use network connections
################################################################################

demoButton(name='PyEdit',
           what='Text file editor',                            # edit myself
           doit='Gui/TextEditor/textEditor.py PyDemos.pyw',    # assume in cwd
           code=['launchmodes.py',
                 'Tools/find.py',
                 'Gui/Tour/scrolledlist.py',          # show in PyEdit viewer        
                 'Gui/ShellGui/formrows.py',          # last = top of stacking
                 'Gui/Tools/guimaker.py',
                 'Gui/TextEditor/textConfig.py',
                 'Gui/TextEditor/textEditor.py'])

demoButton(name='PyView',
           what='Image slideshow, plus note editor',
           doit='Gui/SlideShow/slideShowPlus.py Gui/gifs',
           code=['Gui/Texteditor/textEditor.py',
                 'Gui/SlideShow/slideShow.py',
                 'Gui/SlideShow/slideShowPlus.py'])

demoButton(name='PyDraw',
           what='Draw and move graphics objects',
           doit='Gui/MovingPics/movingpics.py Gui/gifs',
           code=['Gui/MovingPics/movingpics_threads.py',
                 'Gui/MovingPics/movingpics_after.py',
                 'Gui/MovingPics/movingpics.py'])

demoButton(name='PyTree',
           what='Tree data structure viewer',
           doit='Dstruct/TreeView/treeview.py',
           code=['Lang/Parser/parser2.py',
                 'Dstruct/Classics/btree.py',
                 'Dstruct/TreeView/treeview_wrappers.py',
                 'Dstruct/TreeView/treeview.py'])

demoButton(name='PyClock',
           what='Analog/digital clocks',
           doit='Gui/Clock/clockStyles.py Gui/gifs',
           code=['Gui/Tools/windows.py',
                 'Gui/Clock/clockStyles.py',
                 'Gui/Clock/clock.py'])

demoButton(name='PyToe',
           what='Tic-tac-toe game (AI)',
           doit='Ai/TicTacToe/tictactoe.py',
           code=['Ai/TicTacToe/tictactoe_lists.py',
                 'Ai/TicTacToe/tictactoe.py'])

demoButton(name='PyForm',                              # view in-memory dict
           what='Persistent table viewer/editor',      # or cwd shelve of class
           doit='Dbase/TableBrowser/formgui.py',       # 0=do not reinit shelve
          #doit='Dbase/TableBrowser/formtable.py  shelve 0 pyformData-1.5.2',
          #doit='Dbase/TableBrowser/formtable.py  shelve 1 pyformData',
           code=['Dbase/TableBrowser/formtable.py',
                 'Dbase/TableBrowser/formgui.py'])

demoButton(name='PyCalc',
           what='Calculator, plus extensions',
           doit='Lang/Calculator/calculator_plusplus.py',
           code=['Lang/Calculator/calculator_plusplus.py',
                 'Lang/Calculator/calculator_plus_ext.py',
                 'Lang/Calculator/calculator_plus_emb.py',
                 'Lang/Calculator/calculator.py'])

demoButton(name='PyFtp',
           what='Python+Tk ftp clients',
           doit='Internet/Ftp/PyFtpGui.pyw',
           code=['Internet/Sockets/form.py',
                 'Internet/Ftp/putfile.py',
                 'Internet/Ftp/getfile.py',
                 'Internet/Ftp/putfilegui.py',
                 'Internet/Ftp/getfilegui.py',
                 'Internet/Ftp/PyFtpGui.pyw'])

# caveat: PyPhoto requires PIL to be installed: show note
demoButton(name='PyPhoto',
           what='PIL thumbnail image viewer',
           doit='Gui/PIL/pyphoto1.py Gui/PIL/images',     # script, image dir
           code=['Gui/PIL/viewer_thumbs.py',
                 'Gui/PIL/pyphoto1.py',
                 'PyDemos-pil-note.txt'])

# get pymailgui source files by globbing
locat  = 'Internet/Email'
locat2 = locat + '/PyMailGui'

saved  = '%s/SavedMail/savemany-3E.txt' % locat2   # skip savefew-3E
saved += ' %s/SavedMail/i18n-4E %s/SavedMail/version30-4E' % (locat2, locat2)

source = glob.glob(locat + '/mailtools/*.py')   # N source files here + __init__
source+= glob.glob(locat + '/PyMailGui/*.py')   # M source files here + __init__
source+= glob.glob(locat + '/PyMailGui/*.html') # html help file in 2.1
source = [F for F in source if not (
                      os.path.basename(F)[0] == '_' and 
                      os.path.basename(F)[:2] != '__')]  # del tests

demoButton(name='PyMailGUI',
           what='Python+Tk pop/smtp email client',         # open on save files
           doit='%s/PyMailGui.py %s' % (locat2, saved),
           code=(['Gui/Texteditor/textEditor.py',          # lots of sourcecode!
                  'Gui/Tools/windows.py',
                  'Gui/Tools/threadtools.py'] + source) )

################################################################################
# web-based demos - PyInternet opens many smaller demos
################################################################################

# get pymailcgi source files - not incl mailtools!
pagepath = os.getcwd() + '/Internet/Web'
pymailcgifiles = (glob.glob('Internet/Web/PyMailCgi/cgi-bin/*.py') +  # 11 .py
                  ['Internet/Web/PyMailCgi/pymailcgi.html'])          # +root
                                                                      # +server?
if InternetMode == '-file':
    demoButton('PyMailCGI',
               'Browser-based pop/smtp email interface',
               'LaunchBrowser.pyw -file %s/PyMailCgi/pymailcgi.html' % pagepath,
               pymailcgifiles)

    demoButton('PyInternet',
               'Internet-based demo launcher page',
               'LaunchBrowser.pyw -file %s/PyInternetDemos.html' % pagepath,
               ['%s/PyInternetDemos.html' % pagepath]) 

else:
    web80_started = web8000_started = False

    def startLocalWebServers(port):
        """
        on Windows succeeds silently if server already listening
        on the port; caveat: should only run 1 server per port;
        global per-process flag won't fix: the servers live on;

        4E: specialized to use StartArgs on Windows which spawns
        in parallel, seems to work more reliably, and pops up a 
        command prompt shell window to make it more obvious that 
        a server is running and trace its status; also enhanced to
        start a web server only on first select of demo's button;
        """
        global web80_started, web8000_started
        onWin   = sys.platform.startswith('win')
        spawner = launchmodes.StartArgs if onWin else launchmodes.PortableLauncher

        if port == 80 and not web80_started:
            web80_started = True
            spawner('server80', 
                    'Internet/Web/webserver.py Internet/Web')()

        elif port == 8000 and not web8000_started:
            web8000_started = True
            spawner('server8000',
                    'Internet/Web/webserver.py Internet/Web/PyMailCgi 8000')()

    site = 'localhost:%s'
    #startLocalWebServers()   # run webserver on port 80 and 8000 on localhost
    #print('servers started') # now delayed until demo selected in GUI

    class WebLauncher(Launcher):      # customize to start server first
        def run(self, cmdline):
            port, cmdline = cmdline.split('@')
            startLocalWebServers(int(port))
            Launcher.run(self, cmdline)

    demoButton('PyMailCGI',
               'Browser-based pop/smtp email interface',
               '8000@LaunchBrowser.pyw -live pymailcgi.html '+ (site % 8000),
               ['%s/webserver.py' % pagepath] + pymailcgifiles,
               launcher=WebLauncher)

    demoButton('PyInternet',
               'Main Internet demos launcher page',
               '80@LaunchBrowser.pyw -live PyInternetDemos.html ' + (site % 80),
               ['%s/webserver.py' % pagepath,
                '%s/PyInternetDemos.html' % pagepath],
                launcher=WebLauncher)

    # PyErrata removed in 3rd Ed

################################################################################
# toggle info message box font once a second
################################################################################

def refreshMe(info, ncall):
    slant = ['normal', 'italic', 'bold', 'bold italic'][ncall % 4]
    info.config(font=('courier', 20, slant))
    Root.after(1000, (lambda: refreshMe(info, ncall+1)) )

# To try: bind mouse entry events to change info text when over a button

################################################################################
# unhide/hide status box on info clicks
################################################################################

Stat.iconify()
def onInfo():
    if Stat.state() == 'iconic':
        Stat.deiconify()
    else:
        Stat.iconify()  # was 'normal'

################################################################################
# pop up a few web link buttons if connected
################################################################################

radiovar = StringVar() # use a global

def onLinks():
    popup = PopupWindow('PP4E web site links')
    links = [("Book",
                   'LaunchBrowser.pyw -live about-pp.html www.rmi.net/~lutz'),
             ("Python",
                   'LaunchBrowser.pyw -live index.html www.python.org'),
             ("O'Reilly",
                   'LaunchBrowser.pyw -live index.html www.oreilly.com'),
             ("Author",
                   'LaunchBrowser.pyw -live index.html www.rmi.net/~lutz')]

    for (name, command) in links:
        callback = Launcher((name + "'s web site"), command)
        link = Radiobutton(popup, text=name, command=callback)
        link.config(relief=GROOVE, variable=radiovar, value=name)
        link.pack(side=LEFT, expand=YES, fill=BOTH)
    radiovar.set(name)
    Button(popup, text='Quit', command=popup.destroy).pack(expand=YES,fill=BOTH)

    if InternetMode != '-live':
        from tkinter.messagebox import showwarning
        showwarning('PP4E Demos', 'Web links require an Internet connection')

################################################################################
# finish building main GUI, start event loop
################################################################################

Button(Root, text='Info',  command=onInfo).pack(side=TOP, fill=X)
Button(Root, text='Links', command=onLinks).pack(side=TOP, fill=X)
Button(Root, text='Quit',  command=Root.quit).pack(side=BOTTOM, fill=X)
refreshMe(Info, 0)  # start toggling
Root.mainloop()
