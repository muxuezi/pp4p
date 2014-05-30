"""
GUI demo implementation - combines maker, mixin, and this
"""

import sys, os
from tkinter import *                        # widget classes
from PP4E.Gui.Tools.guimixin import *        # mix-in methods: quit, spawn, etc.
from PP4E.Gui.Tools.guimaker import *        # frame, plus menu/toolbar builder

class Hello(GuiMixin, GuiMakerWindowMenu):   # or GuiMakerFrameMenu
    def start(self):
        self.hellos = 0
        self.master.title("GuiMaker Demo")
        self.master.iconname("GuiMaker")
        def spawnme(): self.spawn('big_gui.py')        # defer call vs lambda

        self.menuBar = [                               # a tree: 3 pull downs
          ('File', 0,                                  # (pull-down)
              [('New...',  0, spawnme), 
               ('Open...', 0, self.fileOpen),          # [menu items list]
               ('Quit',    0, self.quit)]              # label,underline,action
          ),

          ('Edit', 0,
              [('Cut',    -1, self.notdone),           # no underline|action
               ('Paste',  -1, self.notdone),           # lambda:0 works too
               'separator',                            # add a separator
               ('Stuff',  -1,
                   [('Clone', -1, self.clone),         # cascaded submenu
                    ('More',  -1, self.more)]
               ),
               ('Delete', -1, lambda:0),
               [5]]                                    # disable 'delete'
          ),

          ('Play', 0,
              [('Hello',     0, self.greeting),
               ('Popup...',  0, self.dialog),
               ('Demos',     0,
                  [('Toplevels', 0,
                       lambda: self.spawn(r'..\Tour\toplevel2.py')),
                   ('Frames',    0,
                       lambda: self.spawn(r'..\Tour\demoAll-frm-ridge.py')),
                   ('Images',    0,
                       lambda: self.spawn(r'..\Tour\buttonpics.py')),
                   ('Alarm',     0,
                       lambda: self.spawn(r'..\Tour\alarm.py', wait=False)),
                   ('Other...', -1, self.pickDemo)]
               )]
          )]

        self.toolBar = [                                     # add 3 buttons
          ('Quit',  self.quit,     dict(side=RIGHT)),        # or {'side': RIGHT}
          ('Hello', self.greeting, dict(side=LEFT)), 
          ('Popup', self.dialog,   dict(side=LEFT, expand=YES)) ]

    def makeWidgets(self):                                   # override default
        middle = Label(self, text='Hello maker world!',      # middle of window 
                       width=40, height=10, 
                       relief=SUNKEN, cursor='pencil', bg='white')
        middle.pack(expand=YES, fill=BOTH)

    def greeting(self):
        self.hellos += 1
        if self.hellos % 3:
            print("hi")
        else:
            self.infobox("Three", 'HELLO!')    # on every third press

    def dialog(self):
        button = self.question('OOPS!',
                               'You typed "rm*" ... continue?',  # old style
                               'questhead', ('yes', 'no'))       # args ignored
        [lambda: None, self.quit][button]()

    def fileOpen(self):
        pick = self.selectOpenFile(file='big_gui.py')
        if pick:
            self.browser(pick)     # browse my source file, or other

    def more(self):
        new = Toplevel()
        Label(new,  text='A new non-modal window').pack()
        Button(new, text='Quit', command=self.quit).pack(side=LEFT)
        Button(new, text='More', command=self.more).pack(side=RIGHT)

    def pickDemo(self):
        pick = self.selectOpenFile(dir='..')
        if pick:
            self.spawn(pick)    # spawn any Python program

if __name__ == '__main__':  Hello().mainloop()   # make one, run one
