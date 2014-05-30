"""
##################################################################################
PyMailGui 3.0 - A Python/tkinter email client.
A client-side tkinter-based GUI interface for sending and receiving email.

See the help string in PyMailGuiHelp.py for usage details, and a list of
enhancements in this version.  

Version 2.0 was a major, complete rewrite.  The changes from 2.0 (July '05)
to 2.1 (Jan '06) were quick-access part buttons on View windows, threaded 
loads and deletes of local save-mail files, and checks for and recovery from 
message numbers out-of-synch with mail server inbox on deletes, index loads,
and message loads.  

Version 3.0 (4E) is a port to Python 3.X; uses grids instead of packed column 
frames for better form layout of headers in view windows; runs update() after 
inserting into a new text editor for accurate line positioning (see PyEdit 
loadFirst changes in Chapter 11); provides an HTML-based version of its help 
text; extracts plain-text from HTML main/only parts for display and quoting; 
supports separators in toolbars; addresses both message content and header 
Unicode/I18N encodings for fetched, sent, and saved mails (see Ch13 and Ch14); 
and much more (see Ch14 for the full rundown on 3.0 upgrades); fetched message 
decoding happens deep in the mailtools package, on mail cache load operations 
here; mailtools also fixes a few email package bugs (see Ch13);

This file implements the top-level windows and interface.  PyMailGui uses a
number of modules that know nothing about this GUI, but perform related tasks,
some of which are developed in other sections of the book.  The mailconfig 
module is expanded for this program.

==Modules defined elsewhere and reused here:==

mailtools (package)
    client-side scripting chapter
    server sends and receives, parsing, construction     (Example 13-21+)
threadtools.py
    GUI tools chapter
    thread queue manangement for GUI callbacks           (Example 10-20)
windows.py
    GUI tools chapter
    border configuration for top-level windows           (Example 10-16)
textEditor.py
    GUI programs chapter
    text widget used in mail view windows, some pop ups  (Example 11-4)

==Generally useful modules defined here:==

popuputil.py
    help and busy windows, for general use
messagecache.py
    a cache that keeps track of mail already loaded
wraplines.py 
    utility for wrapping long lines of messages
html2text.py
    rudimentary HTML parser for extracting plain text
mailconfig.py
    user configuration parameters: server names, fonts, etc.

==Program-specific modules defined here:==

SharedNames.py
    objects shared between window classes and main file
ViewWindows.py
    implementation of view, write, reply, forward windows
ListWindows.py
    implementation of mail-server and local-file list windows
PyMailGuiHelp.py (see also PyMailGuiHelp.html)
    user-visible help text, opened by main window bar
PyMailGui.py
    main, top-level file (run this), with main window types
##################################################################################
"""

import mailconfig, sys
from SharedNames import appname, windows
from ListWindows import PyMailServer, PyMailFile


###############################################################################
# top-level window classes
#
# View, Write, Reply, Forward, Help, BusyBox all inherit from PopupWindow
# directly: only usage;  askpassword calls PopupWindow and attaches;  the
# order matters here!--PyMail classes redef some method defaults in the 
# Window classes, like destroy and okayToExit: must be leftmost;  to use
# PyMailFileWindow standalone, imitate logic in PyMailCommon.onOpenMailFile;
###############################################################################

# uses icon file in cwd or default in tools dir
srvrname = mailconfig.popservername or 'Server'

class PyMailServerWindow(PyMailServer, windows.MainWindow):
    "a Tk, with extra protocol and mixed-in methods"
    def __init__(self):
        windows.MainWindow.__init__(self, appname, srvrname)
        PyMailServer.__init__(self)

class PyMailServerPopup(PyMailServer, windows.PopupWindow):
    "a Toplevel, with extra protocol and mixed-in methods"
    def __init__(self):
        windows.PopupWindow.__init__(self, appname, srvrnane)
        PyMailServer.__init__(self)

class PyMailServerComponent(PyMailServer, windows.ComponentWindow):
    "a Frame, with extra protocol and mixed-in methods"
    def __init__(self):
        windows.ComponentWindow.__init__(self)
        PyMailServer.__init__(self)

class PyMailFileWindow(PyMailFile, windows.PopupWindow):
    "a Toplevel, with extra protocol and mixed-in methods"
    def __init__(self, filename):
        windows.PopupWindow.__init__(self, appname, filename)
        PyMailFile.__init__(self, filename)


###############################################################################
# when run as a top-level program: create main mail-server list window
###############################################################################

if __name__ == '__main__':
    rootwin = PyMailServerWindow()              # open server window
    if len(sys.argv) > 1:                       # 3.0: fix to add len()
        for savename in sys.argv[1:]:
            rootwin.onOpenMailFile(savename)    # open save file windows (demo)
        rootwin.lift()                          # save files loaded in threads
    rootwin.mainloop()
