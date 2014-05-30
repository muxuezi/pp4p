from tkinter import *
from user_preferences import bcolor, bfont, bsize   # get user settings

class ThemedButton(Button):                             
    def __init__(self, parent=None, **configs):         
        Button.__init__(self, parent, **configs)  
        self.pack()      
        self.config(bg=bcolor, font=(bfont, bsize))

def onSpam(): print('Spam')
def onEggs(): print('Eggs')

ThemedButton(text='spam', command=onSpam)  # normal button widget objects 
ThemedButton(text='eggs', command=onEggs)  # all inherit user preferences

class MyButton(ThemedButton):              # subclasses inherit prefs too
    def __init__(self, parent=None, **configs):
        ThemedButton.__init__(self, parent,  **configs)
        self.config(text='subclass')

MyButton(command=onSpam)
mainloop()