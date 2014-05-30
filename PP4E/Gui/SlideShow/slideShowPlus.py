"""
#############################################################################
PyView 1.2: an image slide show with associated text notes.

SlideShow subclass which adds note files with an attached PyEdit object, 
a scale for setting the slideshow delay interval, and a label that gives 
the name of the image file currently being displayed;  

Version 1.2 is a Python 3.x port, but also improves repacking note for 
expansion when it's unhidden, catches note destroys in a subclass to avoid
exceptions when popup window or full component editor has been closed, 
and runs update() before inserting text into newly packed note so it is
positioned correctly at line 1 (see the book's coverage of PyEdit updates).
#############################################################################
"""

import os
from tkinter import *
from PP4E.Gui.TextEditor.textEditor import *
from slideShow import SlideShow
#from slideShow_threads import SlideShow
Size = (300, 550)   # 1.2: start shorter here, (h, w)

class SlideShowPlus(SlideShow):
    def __init__(self, parent, picdir, editclass, msecs=2000, size=Size):
        self.msecs = msecs
        self.editclass = editclass
        SlideShow.__init__(self, parent, picdir, msecs, size)

    def makeWidgets(self):
        self.name = Label(self, text='None', bg='red', relief=RIDGE)
        self.name.pack(fill=X)
        SlideShow.makeWidgets(self)
        Button(self, text='Note', command=self.onNote).pack(fill=X)
        Button(self, text='Help', command=self.onHelp).pack(fill=X)
        s = Scale(label='Speed: msec delay', command=self.onScale,
                  from_=0, to=3000, resolution=50, showvalue=YES,
                  length=400, tickinterval=250, orient='horizontal')
        s.pack(side=BOTTOM, fill=X)
        s.set(self.msecs)

        # 1.2: need to know if editor destroyed, in popup or full component modes
        self.editorGone = False
        class WrapEditor(self.editclass):   # extend PyEdit class to catch Quit
            def onQuit(editor):             # editor is PyEdit instance arg subject
                self.editorGone = True      # self is slide show in enclosing scope
                self.editorUp   = False
                self.editclass.onQuit(editor)       # avoid recursion

        # attach editor frame to window or slideshow frame
        if issubclass(WrapEditor, TextEditorMain):     # make editor now
            self.editor = WrapEditor(self.master)      # need root for menu
        else:
            self.editor = WrapEditor(self)             # embedded or pop-up
        self.editor.pack_forget()                      # hide editor initially
        self.editorUp = self.image = None

    def onStart(self):
        SlideShow.onStart(self)
        self.config(cursor='watch')

    def onStop(self):
        SlideShow.onStop(self)
        self.config(cursor='hand2')

    def onOpen(self):
        SlideShow.onOpen(self)
        if self.image:
            self.name.config(text=os.path.split(self.image[0])[1])
        self.config(cursor='crosshair')
        self.switchNote()

    def quit(self):
        self.saveNote()
        SlideShow.quit(self)

    def drawNext(self):
        SlideShow.drawNext(self)
        if self.image:
            self.name.config(text=os.path.split(self.image[0])[1])
        self.loadNote()

    def onScale(self, value):
        self.msecs = int(value)

    def onNote(self):
        if self.editorGone:                # 1.2: has been destroyed
            return                         # don't rebuild: assume unwanted
        if self.editorUp:
            #self.saveNote()               # if editor already open
            self.editor.pack_forget()      # save text?, hide editor
            self.editorUp = False
        else:
            # 1.2: repack for expansion again, else won't expand now
            # 1.2: update between pack and insert, else @ line 2 initially
            self.editor.pack(side=TOP, expand=YES, fill=BOTH)
            self.editorUp = True           # else unhide/pack editor
            self.update()                  # see Pyedit: same as loadFirst issue
            self.loadNote()                # and load image note text

    def switchNote(self):
        if self.editorUp:
            self.saveNote()                # save current image's note
            self.loadNote()                # load note for new image

    def saveNote(self):
        if self.editorUp:
            currfile = self.editor.getFileName()     # or self.editor.onSave()
            currtext = self.editor.getAllText()      # but text may be empty
            if currfile and currtext:
                try:
                    open(currfile, 'w').write(currtext)
                except:
                    pass  # failure may be normal if run off a cd
 
    def loadNote(self):
        if self.image and self.editorUp:
            root, ext = os.path.splitext(self.image[0])
            notefile  = root + '.note'
            self.editor.setFileName(notefile)
            try:
                self.editor.setAllText(open(notefile).read())
            except:
                self.editor.clearAllText()   # might not have a note

    def onHelp(self):
        showinfo('About PyView',
                 'PyView version 1.2\nMay, 2010\n(1.1 July, 1999)\n'
                 'An image slide show\nProgramming Python 4E')

if __name__ == '__main__':
    import sys
    picdir = '../gifs'
    if len(sys.argv) >= 2:
        picdir = sys.argv[1]

    editstyle = TextEditorComponentMinimal
    if len(sys.argv) == 3:
        try:
            editstyle = [TextEditorMain,
                         TextEditorMainPopup,
                         TextEditorComponent,
                         TextEditorComponentMinimal][int(sys.argv[2])]
        except: pass

    root = Tk()
    root.title('PyView 1.2 - plus text notes')
    Label(root, text="Slide show subclass").pack()
    SlideShowPlus(parent=root, picdir=picdir, editclass=editstyle)
    root.mainloop()
