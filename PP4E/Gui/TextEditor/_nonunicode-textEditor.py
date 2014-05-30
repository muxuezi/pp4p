"""
################################################################################
PyEdit 2.1: a Python/tkinter text file editor and component.

Uses the Tk text widget, plus GuiMaker menus and toolbar buttons to
implement a full-featured text editor that can be run as a standalone
program, and attached as a component to other GUIs.  Also used by
PyMailGUI and PyView to edit mail text and image file notes, and by 
PyMailGUI and PyDemos in pop-up mode to display source and text files.

New in version 2.1:
-updated to run under Python 3.1
-added "grep" search menu option and dialog: threaded external files search
-update change and font dialog implementations to allow many to be open
-verify app exit on quit if changes in other edit windows in process
-runs self.update() before setting text in new editor for loadFirst
-use base name after chdir to run code file, not possibly relative path
-use launch modes that support arguments for run code file mode on Windows
-run code inherits launchmodes backslash conversion (no longer required)

New in version 2.0:
-added simple font components input dialog
-use Tk 8.4 undo stack API to add undo/redo text modifications
-now verifies on quit, open, new, run, only if text modified and unsaved
-searches are case-insensitive now by default
-configuration module for initial font/color/size/searchcase

TBD (and suggested exercises):
-could also allow search case choice in GUI (not just config file)
-could use re patterns for searches (see text chapter)
-could experiment with syntax-directed text colorization (see IDLE)
-could try to verify app exit for quit() in non-managed windows too?
-could queue each result as found in grep dialog thread to avoid delay
-could use images in toolbar buttons (per examples in Chapter 9)

Unicode TBD:
-could open input files in binary mode to better support viewing arbitrary
 Unicode text, but Text content is returned as decoded str whether bytes or 
 str was inserted, so we'd need the encoding type to save or encode (see 
 Chapter 9); as is, clients can still read text as bytes from binary-mode 
 files before creating a texteditor and insert it manually, but file saves 
 may fail if the bytes viewed cannot be encoded per the platform default;
 probably, we need to expect an encoding name to be passed in, or ask the
 user for the encoding if the platform default and common guesses fail;
################################################################################
"""

Version = '2.1'
import sys, os                                    # platform, args, run tools
from tkinter import *                             # base widgets, constants
from tkinter.filedialog   import Open, SaveAs     # standard dialogs
from tkinter.messagebox   import showinfo, showerror, askyesno
from tkinter.simpledialog import askstring, askinteger
from tkinter.colorchooser import askcolor
from PP4E.Gui.Tools.guimaker import *             # Frame + menu/toolbar builders

try:
    import textConfig                        # startup font and colors
    configs = textConfig.__dict__            # work if not on the path or bad
except:
    configs = {}

helptext = """PyEdit version %s
April, 2010
(2.0: January, 2006)
(1.0: October, 2000)

Programming Python, 4th Edition
O'Reilly Media, Inc.

A text editor program and embeddable object
component, written in Python/tkinter.  Use
menu tear-offs and toolbar for quick access
to actions, and Alt-key shortcuts for menus.

Additions in version %s:
- supports Python 3.X
- grep external files search dialog
- allow multiple change and font dialogs
- verify app quit if other edit windows changed

Prior version additions:
- font pick dialog
- unlimited undo/redo
- quit/open/new/run prompt save only if changed
- searches are case-insensitive
- startup configuration module textConfig.py
"""

START     = '1.0'                          # index of first char: row=1,col=0
SEL_FIRST = SEL + '.first'                 # map sel tag to index
SEL_LAST  = SEL + '.last'                  # same as 'sel.last'

FontScale = 0                              # use bigger font on Linux
if sys.platform[:3] != 'win':              # and other non-Windows boxes
    FontScale = 3

################################################################################
# Main class: implements editor GUI, actions
# requires a flavor of GuiMaker to be mixed in by mode specific subclasses;
# not a direct subclass of GuiMaker because that comes in multiple forms.
################################################################################

class TextEditor:                          # mix with menu/toolbar Frame class
    startfiledir = '.'   # for dialogs
    editwindows = []     # for process-wide quit check

    ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance

    colors = [{'fg':'black',      'bg':'white'},      # color pick list
              {'fg':'yellow',     'bg':'black'},      # first item is default
              {'fg':'white',      'bg':'blue'},       # tailor me as desired
              {'fg':'black',      'bg':'beige'},      # or do PickBg/Fg chooser
              {'fg':'yellow',     'bg':'purple'},
              {'fg':'black',      'bg':'brown'},
              {'fg':'lightgreen', 'bg':'darkgreen'},
              {'fg':'darkblue',   'bg':'orange'},
              {'fg':'orange',     'bg':'darkblue'}]

    fonts  = [('courier',    9+FontScale, 'normal'),  # platform-neutral fonts
              ('courier',   12+FontScale, 'normal'),  # (family, size, style)
              ('courier',   10+FontScale, 'bold'),    # or pop up a listbox
              ('courier',   10+FontScale, 'italic'),  # make bigger on Linux
              ('times',     10+FontScale, 'normal'),  # use 'bold italic' for 2
              ('helvetica', 10+FontScale, 'normal'),  # also 'underline', etc.
              ('ariel',     10+FontScale, 'normal'),
              ('system',    10+FontScale, 'normal'),
              ('courier',   20+FontScale, 'normal')]

    def __init__(self, loadFirst=''):
        if not isinstance(self, GuiMaker):
            raise TypeError('TextEditor needs a GuiMaker mixin')
        self.setFileName(None)
        self.lastfind   = None
        self.openDialog = None
        self.saveDialog = None
        self.text.focus()                           # else must click in text
        if loadFirst:
            self.update()                           # 2.1: else @ line 2; see book
            self.onOpen(loadFirst)

    def start(self):                                # run by GuiMaker.__init__
        self.menuBar = [                            # configure menu/toolbar
            ('File', 0,                             # a GuiMaker menu def tree
                 [('Open...',    0, self.onOpen),   # build in method for self
                  ('Save',       0, self.onSave),   # label, shortcut, callback
                  ('Save As...', 5, self.onSaveAs),
                  ('New',        0, self.onNew),
                  'separator',
                  ('Quit...',    0, self.onQuit)]
            ),
            ('Edit', 0,
                 [('Undo',       0, self.onUndo),
                  ('Redo',       0, self.onRedo),
                  'separator',
                  ('Cut',        0, self.onCut),
                  ('Copy',       1, self.onCopy),
                  ('Paste',      0, self.onPaste),
                  'separator',
                  ('Delete',     0, self.onDelete),
                  ('Select All', 0, self.onSelectAll)]
            ),
            ('Search', 0,
                 [('Goto...',    0, self.onGoto),
                  ('Find...',    0, self.onFind),
                  ('Refind',     0, self.onRefind),
                  ('Change...',  0, self.onChange),
                  ('Grep...',    3, self.onGrep)]
            ),
            ('Tools', 0,
                 [('Pick Font...', 6, self.onPickFont),
                  ('Font List',    0, self.onFontList),
                  'separator',
                  ('Pick Bg...',   3, self.onPickBg),
                  ('Pick Fg...',   0, self.onPickFg),
                  ('Color List',   0, self.onColorList),
                  'separator',
                  ('Info...',      0, self.onInfo),
                  ('Clone',        1, self.onClone),
                  ('Run Code',     0, self.onRunCode)]
            )]
        self.toolBar = [
            ('Save',  self.onSave,   {'side': LEFT}),
            ('Cut',   self.onCut,    {'side': LEFT}),
            ('Copy',  self.onCopy,   {'side': LEFT}),
            ('Paste', self.onPaste,  {'side': LEFT}),
            ('Find',  self.onRefind, {'side': LEFT}),
            ('Help',  self.help,     {'side': RIGHT}),
            ('Quit',  self.onQuit,   {'side': RIGHT})]

    def makeWidgets(self):                          # run by GuiMaker.__init__
        name = Label(self, bg='black', fg='white')  # add below menu, above tool
        name.pack(side=TOP, fill=X)                 # menu/toolbars are packed
                                                    # GuiMaker frame packs itself
        vbar  = Scrollbar(self)
        hbar  = Scrollbar(self, orient='horizontal')
        text  = Text(self, padx=5, wrap='none')        # disable line wrapping
        text.config(undo=1, autoseparators=1)          # 2.0, default is 0, 1

        vbar.pack(side=RIGHT,  fill=Y)
        hbar.pack(side=BOTTOM, fill=X)                 # pack text last
        text.pack(side=TOP,    fill=BOTH, expand=YES)  # else sbars clipped

        text.config(yscrollcommand=vbar.set)    # call vbar.set on text move
        text.config(xscrollcommand=hbar.set)
        vbar.config(command=text.yview)         # call text.yview on scroll move
        hbar.config(command=text.xview)         # or hbar['command']=text.xview

        # 2.0: apply user configs or defaults
        startfont = configs.get('font', self.fonts[0])
        startbg   = configs.get('bg',   self.colors[0]['bg'])
        startfg   = configs.get('fg',   self.colors[0]['fg'])
        text.config(font=startfont, bg=startbg, fg=startfg)
        if 'height' in configs: text.config(height=configs['height'])
        if 'width'  in configs: text.config(width =configs['width'])
        self.text = text
        self.filelabel = name

    ############################################################################
    # File menu commands
    ############################################################################

    def my_askopenfilename(self):      # objects remember last result dir/file
        if not self.openDialog:
           self.openDialog = Open(initialdir=self.startfiledir,
                                  filetypes=self.ftypes)
        return self.openDialog.show()

    def my_asksaveasfilename(self):    # objects remember last result dir/file
        if not self.saveDialog:
           self.saveDialog = SaveAs(initialdir=self.startfiledir,
                                    filetypes=self.ftypes)
        return self.saveDialog.show()

    def onOpen(self, loadFirst=''):
        doit = (not self.text_edit_modified() or      # 2.0
                askyesno('PyEdit', 'Text has changed: discard changes?'))
        if doit:
            file = loadFirst or self.my_askopenfilename()
            if file:
                try:
                    text = open(file, 'r').read()
                except:
                    showerror('PyEdit', 'Could not open file ' + file)
                else:
                    self.setAllText(text)
                    self.setFileName(file)
                    self.text.edit_reset()          # 2.0: clear undo/redo stks
                    self.text.edit_modified(0)      # 2.0: clear modified flag

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None

    def onSaveAs(self, forcefile=None):
        file = forcefile or self.my_asksaveasfilename()
        if file:
            text = self.getAllText()
            try:
                open(file, 'w').write(text)
            except:
                showerror('PyEdit', 'Could not write file ' + file)
            else:
                self.setFileName(file)             # may be newly created
                self.text.edit_modified(0)         # 2.0: clear modified flag
                                                   # don't clear undo/redo stks
    def onNew(self):
        doit = (not self.text_edit_modified() or   # 2.0
                askyesno('PyEdit', 'Text has changed: discard changes?'))
        if doit:
            self.setFileName(None)
            self.clearAllText()
            self.text.edit_reset()                 # 2.0: clear undo/redo stks
            self.text.edit_modified(0)             # 2.0: clear modified flag

    def onQuit(self):
        """
        on Quit menu/toolbar select and wm border X button in toplevel windows;
        2.1: don't exit app if others changed;  2.0: don't ask if self unchanged;
        moved to the top-level window classes at the end since may vary per usage:
        a Quit in GUI might quit() to exit, destroy() just one Toplevel, Tk, or 
        edit frame, or not be provided at all when run as an attached component;
        check self for changes, and if might quit(), main windows should check
        other windows in the process-wide list to see if they have changed too; 
        """
        assert False, 'onQuit must be defined in window-specific sublass' 

    def text_edit_modified(self):
        """
        2.1: this now works! seems to have been a bool result type issue in tkinter;
        2.0: self.text.edit_modified() broken in Python 2.4: do manually for now; 
        """
        return self.text.edit_modified()
       #return self.tk.call((self.text._w, 'edit') + ('modified', None))

    ############################################################################
    # Edit menu commands
    ############################################################################

    def onUndo(self):                           # 2.0
        try:                                    # tk8.4 keeps undo/redo stacks
            self.text.edit_undo()               # exception if stacks empty
        except TclError:                        # menu tear-offs for quick undo
            showinfo('PyEdit', 'Nothing to undo')

    def onRedo(self):                           # 2.0: redo an undone
        try:
            self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')

    def onCopy(self):                           # get text selected by mouse, etc.
        if not self.text.tag_ranges(SEL):       # save in cross-app clipboard
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onDelete(self):                         # delete selected text, no save
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.onCopy()                       # save and delete selected text
            self.onDelete()

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('PyEdit', 'Nothing to paste')
            return
        self.text.insert(INSERT, text)          # add at current insert cursor
        self.text.tag_remove(SEL, '1.0', END)
        self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.text.see(INSERT)                   # select it, so it can be cut

    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END+'-1c')   # select entire text
        self.text.mark_set(INSERT, '1.0')          # move insert point to top
        self.text.see(INSERT)                      # scroll to top

    ############################################################################
    # Search menu commands
    ############################################################################

    def onGoto(self, forceline=None):
        line = forceline or askinteger('PyEdit', 'Enter line number')
        self.text.update()
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END+'-1c')
            maxline  = int(maxindex.split('.')[0])
            if line > 0 and line <= maxline:
                self.text.mark_set(INSERT, '%d.0' % line)      # goto line
                self.text.tag_remove(SEL, '1.0', END)          # delete selects
                self.text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
                self.text.see(INSERT)                          # scroll to line
            else:
                showerror('PyEdit', 'Bad line number')

    def onFind(self, lastkey=None):
        key = lastkey or askstring('PyEdit', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind = key
        if key:                                                    # 2.0: nocase
            nocase = configs.get('caseinsens', True)               # 2.0: config
            where = self.text.search(key, INSERT, END, nocase=nocase)
            if not where:                                          # don't wrap
                showerror('PyEdit', 'String not found')
            else:
                pastkey = where + '+%dc' % len(key)           # index past key
                self.text.tag_remove(SEL, '1.0', END)         # remove any sel
                self.text.tag_add(SEL, where, pastkey)        # select key
                self.text.mark_set(INSERT, pastkey)           # for next find
                self.text.see(where)                          # scroll display

    def onRefind(self):
        self.onFind(self.lastfind)

    def onChange(self):
        """
        non-modal find/change dialog 
        2.1: pass per-dialog inputs to callbacks, may be > 1 change dialog open
        """
        new = Toplevel(self)
        new.title('PyEdit - change')
        Label(new, text='Find text?', relief=RIDGE, width=15).grid(row=0, column=0)
        Label(new, text='Change to?', relief=RIDGE, width=15).grid(row=1, column=0)
        entry1 = Entry(new)
        entry2 = Entry(new)
        entry1.grid(row=0, column=1, sticky=EW)
        entry2.grid(row=1, column=1, sticky=EW)

        def onFind():                         # use my entry in enclosing scope   
            self.onFind(entry1.get())         # runs normal find dialog callback

        def onApply():
            self.onDoChange(entry1.get(), entry2.get())

        Button(new, text='Find',  command=onFind ).grid(row=0, column=2, sticky=EW)
        Button(new, text='Apply', command=onApply).grid(row=1, column=2, sticky=EW)
        new.columnconfigure(1, weight=1)      # expandable entries

    def onDoChange(self, findtext, changeto):
        # on Apply in change dialog: change and refind
        if self.text.tag_ranges(SEL):                      # must find first
            self.text.delete(SEL_FIRST, SEL_LAST)          
            self.text.insert(INSERT, changeto)             # deletes if empty
            self.text.see(INSERT)
            self.onFind(findtext)                          # goto next appear
            self.text.update()                             # force refresh

    def onGrep(self):
        """
        new in version 2.1: threaded external file search;
        search matched filenames in directory tree for string;
        listbox clicks open matched file at line of occurrence;
        search is threaded so the GUI remains active and is not
        blocked, and to allow multiple greps to overlap in time;
        could use threadtools, but avoid loop in no active grep;
        """
        from PP4E.Gui.ShellGui.formrows import makeFormRow

        # nonmodal dialog: get dirnname, filenamepatt, grepkey
        popup = Toplevel()
        popup.title('PyEdit - grep')
        var1 = makeFormRow(popup, label='Directory root',   width=18, browse=False)
        var2 = makeFormRow(popup, label='Filename pattern', width=18, browse=False)
        var3 = makeFormRow(popup, label='Search string',    width=18, browse=False)
        var1.set('.')      # current dir
        var2.set('*.py')   # initial values
        Button(popup, text='Go',
           command=lambda: self.onDoGrep(var1.get(), var2.get(), var3.get())).pack()

    def onDoGrep(self, dirname, filenamepatt, grepkey):
        # on Go in grep dialog: populate scrolled list with matches
        # tbd: should producer thread be daemon so dies with app?
        import threading, queue

        # make non-modal un-closeable dialog
        mypopup = Tk()
        mypopup.title('PyEdit - grepping')
        status = Label(mypopup, text='Grep thread searching for: %r...' % grepkey)
        status.pack(padx=20, pady=20)
        mypopup.protocol('WM_DELETE_WINDOW', lambda: None)  # ignore X close

        # start producer thread, consumer loop
        myqueue = queue.Queue()
        threadargs = (filenamepatt, dirname, grepkey, myqueue)
        threading.Thread(target=self.grepThreadProducer, args=threadargs).start()
        self.grepThreadConsumer(grepkey, myqueue, mypopup)

    def grepThreadProducer(self, filenamepatt, dirname, grepkey, myqueue):
        """
        in a non-GUI parallel thread: queue find.find results list;
        could also queue matches as found, but need to keep window;
        """
        from PP4E.Tools.find import find
        matches = []
        for filepath in find(pattern=filenamepatt, startdir=dirname):
            try:
                for (linenum, linestr) in enumerate(open(filepath)):
                    if grepkey in linestr:
                        message = '%s@%d  [%s]' % (filepath, linenum + 1, linestr)
                        matches.append(message)
            except UnicodeDecodeError:
                print('Unicode error in:', filepath)
        myqueue.put(matches)

    def grepThreadConsumer(self, grepkey, myqueue, mypopup):
        """
        in the main GUI thread: watch queue for results or [];
        there may be multiple active grep threads/loops/queues;
        there may be other types of threads/checkers in process,
        especially when PyEdit is attached component (PyMailGUI);
        """
        import queue
        try:
            matches = myqueue.get(block=False)
        except queue.Empty:
            self.after(250, self.grepThreadConsumer, grepkey, myqueue, mypopup)
        else:
            mypopup.destroy()     # close status
            self.update()         # erase it now
            if not matches:
                showinfo('PyEdit', 'Grep found no matches for: %r' % grepkey)
            else:
                self.grepMatchesList(matches, grepkey)

    def grepMatchesList(self, matches, grepkey):
        # populate list after successful matches
        from PP4E.Gui.Tour.scrolledlist import ScrolledList
        print('Matches for %s: %s' % (grepkey, len(matches)))

        # catch list double-click
        class ScrolledFilenames(ScrolledList):
            def runCommand(self, selection):  
                file, line = selection.split('  [', 1)[0].split('@')
                editor = TextEditorMainPopup(loadFirst=file, winTitle=' grep match')
                editor.onGoto(int(line))
                editor.text.focus_force()   # no, really

        # new non-modal widnow
        popup = Tk()
        popup.title('PyEdit - grep matches: %r' % grepkey)
        ScrolledFilenames(parent=popup, options=matches)


    ############################################################################
    # Tools menu commands
    ############################################################################

    def onFontList(self):
        self.fonts.append(self.fonts[0])           # pick next font in list
        del self.fonts[0]                          # resizes the text area
        self.text.config(font=self.fonts[0])

    def onColorList(self):
        self.colors.append(self.colors[0])         # pick next color in list
        del self.colors[0]                         # move current to end
        self.text.config(fg=self.colors[0]['fg'], bg=self.colors[0]['bg'])

    def onPickFg(self):
        self.pickColor('fg')                       # added on 10/02/00

    def onPickBg(self):                            # select arbitrary color
        self.pickColor('bg')                       # in standard color dialog

    def pickColor(self, part):                     # this is too easy
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(**{part: hexstr})

    def onInfo(self):
        text  = self.getAllText()                  # added on 5/3/00 in 15 mins
        bytes = len(text)                          # words uses a simple guess:
        lines = len(text.split('\n'))              # any separated by whitespace
        words = len(text.split())                  # 3.x: bytes is really chars
        index = self.text.index(INSERT)            # str is unicode code points
        where = tuple(index.split('.'))
        showinfo('PyEdit Information',
                 'Current location:\n\n' +
                 'line:\t%s\ncolumn:\t%s\n\n' % where +
                 'File text statistics:\n\n' +
                 'chars:\t%d\nlines:\t%d\nwords:\t%d\n' % (bytes, lines, words))

    def onClone(self):                  
        """
        open a new edit window without changing one already open
        inherits quit and other behavior of window that it clones
        """
        new = Toplevel()                # a new edit window in same process
        myclass = self.__class__        # instance's (lowest) class object
        myclass(new)                    # attach/run instance of my class

    def onRunCode(self, parallelmode=True):
        """
        run Python code being edited--not an IDE, but handy;
        tries to run in file's dir, not cwd (may be PP4E root);
        inputs and adds command-line arguments for script files;
        code's stdin/out/err = editor's start window, if any:
        run with a console window to see code's print outputs;
        but parallelmode uses start to open a DOS box for I/O;
        module search path will include '.' dir where started;
        in non-file mode, code's Tk root may be PyEdit's window;
        subprocess or multiprocessing modules may work here too;
        2.1: fixed to use base file name after chdir, not path;
        2.1: use StartArs to allow args in file mode on Windows;
        """
        def askcmdargs():
            return askstring('PyEdit', 'Commandline arguments?') or ''

        from PP4E.launchmodes import System, Start, StartArgs, Fork
        filemode = False
        thefile  = str(self.getFileName())
        if os.path.exists(thefile):
            filemode = askyesno('PyEdit', 'Run from file?')
        if not filemode:                                    # run text string
            cmdargs   = askcmdargs()
            namespace = {'__name__': '__main__'}            # run as top-level
            sys.argv  = [thefile] + cmdargs.split()         # could use threads
            exec(self.getAllText() + '\n', namespace)       # exceptions ignored
        elif self.text_edit_modified():                     # 2.0: changed test
            showerror('PyEdit', 'Text changed: save before run')
        else:
            cmdargs = askcmdargs()
            mycwd   = os.getcwd()                           # cwd may be root
            dirname, filename = os.path.split(thefile)      # get dir, base
            os.chdir(dirname or mycwd)                      # cd for filenames
            thecmd  = filename + ' ' + cmdargs              # 2.1: not theFile
            if not parallelmode:                            # run as file
                System(thecmd, thecmd)()                    # block editor
            else:
                if sys.platform[:3] == 'win':               # spawn in parallel
                    run = StartArgs if cmdargs else Start   # 2.1: support args
                    run(thecmd, thecmd)()                   # or always Spawn
                else:
                    Fork(thecmd, thecmd)()                  # spawn in parallel
            os.chdir(mycwd)                                 # go back to my dir

    def onPickFont(self):
        """
        2.0 non-modal font spec dialog
        2.1: pass per-dialog inputs to callback, may be > 1 font dialog open
        """
        from PP4E.Gui.ShellGui.formrows import makeFormRow
        popup = Toplevel(self)
        popup.title('PyEdit - font')
        var1 = makeFormRow(popup, label='Family', browse=False)
        var2 = makeFormRow(popup, label='Size',   browse=False)
        var3 = makeFormRow(popup, label='Style',  browse=False)
        var1.set('courier')
        var2.set('12')              # suggested vals
        var3.set('bold italic')     # see pick list for valid inputs
        Button(popup, text='Apply', command=
               lambda: self.onDoFont(var1.get(), var2.get(), var3.get())).pack()

    def onDoFont(self, family, size, style):
        try:  
            self.text.config(font=(family, int(size), style))
        except:
            showerror('PyEdit', 'Bad font specification')

    ############################################################################
    # Utilities, useful outside this class
    ############################################################################

    def isEmpty(self):
        return not self.getAllText()

    def getAllText(self):
        return self.text.get('1.0', END+'-1c')  # extract text as a string
    def setAllText(self, text):
        self.text.delete('1.0', END)            # store text string in widget
        self.text.insert(END, text)             # or '1.0'
        self.text.mark_set(INSERT, '1.0')       # move insert point to top
        self.text.see(INSERT)                   # scroll to top, insert set
    def clearAllText(self):
        self.text.delete('1.0', END)            # clear text in widget

    def getFileName(self):
        return self.currfile
    def setFileName(self, name):                # also: onGoto(linenum)
        self.currfile = name  # for save
        self.filelabel.config(text=str(name))

    def setBg(self, color):
        self.text.config(bg=color)              # to set manually from code
    def setFg(self, color):
        self.text.config(fg=color)              # 'black', hexstring
    def setFont(self, font):
        self.text.config(font=font)             # ('family', size, 'style')

    def setHeight(self, lines):                 # default = 24h x 80w
        self.text.config(height=lines)          # may also be from textCongif.py
    def setWidth(self, chars):
        self.text.config(width=chars)

    def clearModified(self):
        self.text.edit_modified(0)              # clear modified flag
    def isModified(self):
        return self.text_edit_modified()        # changed since last reset?

    def help(self):
        showinfo('About PyEdit', helptext % ((Version,)*2))

################################################################################
# Ready-to-use editor classes
# mix in a GuiMaker Frame subclass which builds menu and toolbars
#
# these classes are common use cases, but other configurations are possible;
# call TextEditorMain().mainloop() to start PyEdit as a standalone program;
# redefine/extend onQuit in a subclass to catch exit or destroy (see PyView);
# caveat: could use windows.py for icons, but quit protocol is custom here.
################################################################################

# 2.1: on quit(), don't silently exit entire app if any other changed edit
# windows are open in the process - changes would be lost because all other 
# windows are closed too, including multiple Tk editor parents;  uses a list
# to keep track of all PyEdit window instances open in process; this may be 
# too broad (if we destroy() instead of quit(), need only check check children
# of parent being destroyed), but better to err on side of being too inclusive;
# onQuit moved here because varies per window type and is not present for all;
#
# assumes a TextEditorMainPopup is never a parent to other editor windows -
# Toplevel children are destroyed with their parents;  this does not address 
# closes outside the scope of PyEdit classes here (tkinter quit is available 
# on every widget, and any widget type may be a Toplevel parent!);  client is
# responsible for checking for editor content changes in all uncovered cases;
# note that tkinter's <Destroy> bind event won't help here, because its callback
# cannot run GUI operations such as text change tests and fetches - see the 
# book and destroyer.py for more details on this event;

#
# when editor owns the window
#

class TextEditorMain(TextEditor, GuiMakerWindowMenu):
    """
    main PyEdit windows that quit() to exit app on a Quit in GUI, and build
    a menu on a window;  parent may be default Tk, explicit Tk, or Toplevel: 
    parent must be a window, and probably should be a Tk so this isn't silently
    destoyed and closed with a parent;  all main PyEdit windows check all other
    PyEdit windows open in the process for changes on a Quit in the GUI, since 
    a quit() here will exit the entire app;  the editor's frame need not occupy 
    entire window (may have other parts: see PyView), but its Quit ends program;
    onQuit is run for Quit in toolbar or File menu, as well as window border X;
    """
    def __init__(self, parent=None, loadFirst=''):       # when fills whole window
        GuiMaker.__init__(self, parent)                  # use main window menus
        TextEditor.__init__(self, loadFirst)             # GuiMaker frame packs self
        self.master.title('PyEdit ' + Version)           # title, wm X if standalone
        self.master.iconname('PyEdit')
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)
        TextEditor.editwindows.append(self)

    def onQuit(self):                              # on a Quit request in the GUI
        close = not self.text_edit_modified()      # check self, ask?, check others
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            windows = TextEditor.editwindows
            changed = [w for w in windows if w != self and w.text_edit_modified()]
            if not changed:
                GuiMaker.quit(self) # quit ends entire app regardless of widget type
            else:
                numchange = len(changed)
                verify = '%s other edit window%s changed: quit and discard anyhow?'
                verify = verify % (numchange, 's' if numchange > 1 else '')
                if askyesno('PyEdit', verify):
                    GuiMaker.quit(self)

class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    """
    popup PyEdit windows that destroy() to close only self on a Quit in GUI,
    and build a menu on a window;  makes own Toplevel parent, which is child
    to default Tk (for None) or other passed-in window or widget (e.g., a frame);
    adds to list so will be checked for changes if any PyEdit main window quits;
    if any PyEdit main windows will be created, parent of this should also be a 
    PyEdit main window's parent so this is not closed silently while being tracked;
    onQuit is run for Quit in toolbar or File menu, as well as window border X;
    """
    def __init__(self, parent=None, loadFirst='', winTitle=''):
        self.popup = Toplevel(parent)                   # create own window
        GuiMaker.__init__(self, self.popup)             # use main window menus
        TextEditor.__init__(self, loadFirst)            # a frame in a new popup
        assert self.master == self.popup
        self.popup.title('PyEdit ' + Version + winTitle)
        self.popup.iconname('PyEdit')
        self.popup.protocol('WM_DELETE_WINDOW', self.onQuit)
        TextEditor.editwindows.append(self)

    def onQuit(self):
        close = not self.text_edit_modified()
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close: 
            self.popup.destroy()                       # kill this window only
            TextEditor.editwindows.remove(self)        # (plus any child windows)

#
# when editor embedded in another window
#

class TextEditorComponent(TextEditor, GuiMakerFrameMenu):
    """
    attached PyEdit component frames with full menu/toolbar options,
    which run a destroy() on a Quit in the GUI to erase self only;
    a Quit in the GUI verifies if any changes in self (only) here;
    does not intercept window manager border X: doesn't own window;
    does not add self to changes tracking list: part of larger app;
    """
    def __init__(self, parent=None, loadFirst=''):     # use Frame-based menus
        GuiMaker.__init__(self, parent)                # all menus, buttons on
        TextEditor.__init__(self, loadFirst)           # GuiMaker must init 1st

    def onQuit(self):
        close = not self.text_edit_modified()
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            self.destroy()   # erase self Frame but do not quit enclosing app

class TextEditorComponentMinimal(TextEditor, GuiMakerFrameMenu):
    """
    attached PyEdit component frames without Quit and File menu options;
    on startup, removes Quit from toolbar, and either deletes File menu 
    or disables all its items (possibly hackish, but sufficient); menu and 
    toolbar structures are per-instance data: changes do not impact others;
    Quit in GUI never occurs, because it is removed from available options;
    """
    def __init__(self, parent=None, loadFirst='', deleteFile=True):
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)                # GuiMaker frame packs self
        TextEditor.__init__(self, loadFirst)           # TextEditor adds middle

    def start(self):
        TextEditor.start(self)                         # GuiMaker start call
        for i in range(len(self.toolBar)):             # delete quit in toolbar
            if self.toolBar[i][0] == 'Quit':           # delete file menu items,
                del self.toolBar[i]                    # or just disable file
                break
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]
                    break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':
                    items.append([1,2,3,4,6])

################################################################################
# standalone program run
################################################################################

def testPopup():
    # see PyView and PyMail for component tests
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()

def main():                                           # may be typed or clicked
    try:                                              # or associated on Windows
        fname = sys.argv[1]                           # arg = optional filename
    except IndexError:                                # build in default Tk root
        fname = None
    TextEditorMain(loadFirst=fname).pack(expand=YES, fill=BOTH)
    mainloop()

if __name__ == '__main__':                            # when run as a script
    #testPopup()
    main()                                            # run .pyw for no DOS box
