"""
wrap up widget construction in functions for easier use, making some
assumptions (e.g., expansion); use extras kw args for width, font/color
"""

from tkinter import *
     
def frame(root, side=TOP, **extras): 
    widget = Frame(root)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: widget.config(**extras)
    return widget
     
def label(root, side, text, **extras):
    widget = Label(root, text=text, relief=RIDGE)        # default config
    widget.pack(side=side, expand=YES, fill=BOTH)        # pack automatically
    if extras: widget.config(**extras)                   # apply any extras
    return widget
     
def button(root, side, text, command, **extras): 
    widget = Button(root, text=text, command=command) 
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: widget.config(**extras)
    return widget
     
def entry(root, side, linkvar, **extras):
    widget = Entry(root, relief=SUNKEN, textvariable=linkvar)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: widget.config(**extras)
    return widget

if __name__ == '__main__':
    app = Tk()
    frm = frame(app, TOP)               # much less code required here!
    label(frm, LEFT, 'SPAM')
    button(frm, BOTTOM, 'Press', lambda: print('Pushed'))
    mainloop()