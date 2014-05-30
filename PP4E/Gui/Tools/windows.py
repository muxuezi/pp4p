"""
###############################################################################
Classes that encapsulate top-level interfaces.
Allows same GUI to be main, pop-up, or attached; content classes may inherit
from these directly, or be mixed together with them per usage mode; may also
be called directly without a subclass; designed to be mixed in after (further
to the right than) app-specific classes: else, subclass gets methods here
(destroy, okayToQuit), instead of from app-specific classes--can't redefine.
###############################################################################
"""

import os, glob
from tkinter import Tk, Toplevel, Frame, YES, BOTH, RIDGE
from tkinter.messagebox import showinfo, askyesno

class _window:
    """
    mixin shared by main and pop-up windows
    """
    foundicon = None                                       # shared by all inst
    iconpatt  = '*.ico'                                    # may be reset
    iconmine  = 'py.ico'

    def configBorders(self, app, kind, iconfile):
        if not iconfile:                                   # no icon passed?
            iconfile = self.findIcon()                     # try curr,tool dirs
        title = app
        if kind: title += ' - ' + kind
        self.title(title)                                  # on window border
        self.iconname(app)                                 # when minimized
        if iconfile:
            try:
                self.iconbitmap(iconfile)                  # window icon image
            except:                                        # bad py or platform
                pass
        self.protocol('WM_DELETE_WINDOW', self.quit)       # don't close silent

    def findIcon(self):
        if _window.foundicon:                              # already found one?
            return _window.foundicon
        iconfile  = None                                   # try curr dir first
        iconshere = glob.glob(self.iconpatt)               # assume just one
        if iconshere:                                      # del icon for red Tk
            iconfile = iconshere[0]
        else:                                              # try tools dir icon
            mymod  = __import__(__name__)                  # import self for dir
            path   = __name__.split('.')                   # poss a package path
            for mod in path[1:]:                           # follow path to end
                mymod = getattr(mymod, mod)                # only have leftmost
            mydir  = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.iconmine)    # use myicon, not tk
            if os.path.exists(myicon): iconfile = myicon
        _window.foundicon = iconfile                       # don't search again
        return iconfile

class MainWindow(Tk, _window):
    """
    when run in main top-level window
    """
    def __init__(self, app, kind='', iconfile=None):
        self.findIcon()
        Tk.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):
        if self.okayToQuit():                                # threads running?
            if askyesno(self.__app, 'Verify Quit Program?'):
                self.destroy()                               # quit whole app
        else:
            showinfo(self.__app, 'Quit not allowed')         # or in okayToQuit?

    def destroy(self):                                       # exit app silently
        Tk.quit(self)                                        # redef if exit ops

    def okayToQuit(self):                                    # redef me if used
        return True                                          # e.g., thread busy

class PopupWindow(Toplevel, _window):
    """
    when run in secondary pop-up window
    """
    def __init__(self, app, kind='', iconfile=None):
        Toplevel.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):                                        # redef me to change
        if askyesno(self.__app, 'Verify Quit Window?'):    # or call destroy
            self.destroy()                                 # quit this window

    def destroy(self):                                     # close win silently
        Toplevel.destroy(self)                             # redef for close ops

class QuietPopupWindow(PopupWindow):
    def quit(self):
        self.destroy()                                     # don't verify close

class ComponentWindow(Frame):
    """
    when attached to another display
    """
    def __init__(self, parent):                            # if not a frame
        Frame.__init__(self, parent)                       # provide container
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=RIDGE, border=2)                # reconfig to change

    def quit(self):
        showinfo('Quit', 'Not supported in attachment mode')

    # destroy from Frame: erase frame silent               # redef for close ops
