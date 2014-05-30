# reload callback handlers dynamically

from tkinter import *
import radactions           # get initial callback handlers
from imp import reload      # moved to a module in Python 3.X

class Hello(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        Button(self, text='message1', command=self.message1).pack(side=LEFT)
        Button(self, text='message2', command=self.message2).pack(side=RIGHT)

    def message1(self):
        reload(radactions)         # need to reload actions module before calling
        radactions.message1()      # now new version triggered by pressing button

    def message2(self):
        reload(radactions)         # changes to radactions.py picked up by reload
        radactions.message2(self)  # call the most recent version; pass self

    def method1(self):
        print('exposed method...')       # called from radactions function

Hello().mainloop()
