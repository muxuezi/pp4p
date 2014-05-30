#!/usr/local/bin/python
"""
same but add photos in toolbar using PIL to generate images
"""

from tkinter import *                              # get widget classes
from tkinter.messagebox import *                   # get standard dialogs

class NewMenuDemo(Frame):                          # an extended frame
    def __init__(self, parent=None):               # attach to top-level?
        Frame.__init__(self, parent)               # do superclass init
        self.pack(expand=YES, fill=BOTH)
        self.createWidgets()                       # attach frames/widgets
        self.master.title("Toolbars and Menus")    # set window-manager info
        self.master.iconname("tkpython")           # label when iconified

    def createWidgets(self):
        self.makeMenuBar()
        self.makeToolBar()
        L = Label(self, text='Menu and Toolbar Demo')
        L.config(relief=SUNKEN, width=40, height=10, bg='white')
        L.pack(expand=YES, fill=BOTH)

    #def makeToolBar(self):
    #    toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
    #    toolbar.pack(side=BOTTOM, fill=X)
    #    Button(toolbar, text='Quit',  command=self.quit    ).pack(side=RIGHT)
    #    Button(toolbar, text='Hello', command=self.greeting).pack(side=LEFT)

    def makeToolBar(self, size=(40, 40)):
        from PIL.ImageTk import PhotoImage, Image     # if jpegs or make new thumbs
        imgdir = r'../PIL/images/'
        toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
        toolbar.pack(side=BOTTOM, fill=X)
        photos = 'ora-lp4e-big.jpg', 'PythonPoweredAnim.gif', 'python_conf_ora.gif'
        self.toolPhotoObjs = []
        for file in photos:
            imgobj = Image.open(imgdir + file)        # make new thumb
            imgobj.thumbnail(size, Image.ANTIALIAS)   # best downsize filter
            img = PhotoImage(imgobj)
            btn = Button(toolbar, image=img, command=self.greeting)
            btn.config(relief=RAISED, bd=2)
            btn.config(width=size[0], height=size[1])
            btn.pack(side=LEFT)
            self.toolPhotoObjs.append((img, imgobj))  # keep a reference
        Button(toolbar, text='Quit', command=self.quit).pack(side=RIGHT, fill=Y)

    def makeMenuBar(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)    # master=top-level window
        self.fileMenu()
        self.editMenu()
        self.imageMenu()

    def fileMenu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Open...', command=self.notdone)
        pulldown.add_command(label='Quit',    command=self.quit)
        self.menubar.add_cascade(label='File', underline=0, menu=pulldown)

    def editMenu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Paste',   command=self.notdone)
        pulldown.add_command(label='Spam',    command=self.greeting)
        pulldown.add_separator()
        pulldown.add_command(label='Delete',  command=self.greeting)
        pulldown.entryconfig(4, state=DISABLED)
        self.menubar.add_cascade(label='Edit', underline=0, menu=pulldown)

    def imageMenu(self):
        photoFiles = ('ora-lp4e.gif', 'pythonPowered.gif', 'python_conf_ora.gif')
        pulldown = Menu(self.menubar)
        self.photoObjs = []
        for file in photoFiles:
            img = PhotoImage(file='../gifs/' + file)
            pulldown.add_command(image=img, command=self.notdone)
            self.photoObjs.append(img)   # keep a reference
        self.menubar.add_cascade(label='Image', underline=0, menu=pulldown)

    def greeting(self):
        showinfo('greeting', 'Greetings')
    def notdone(self):
        showerror('Not implemented', 'Not yet available')
    def quit(self):
        if askyesno('Verify quit', 'Are you sure you want to quit?'):
            Frame.quit(self)

if __name__ == '__main__':  NewMenuDemo().mainloop()  # if I'm run as a script
