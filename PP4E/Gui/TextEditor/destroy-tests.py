# quit, destroy, and window parents and widgets

from tkinter import *

for ix, cls in enumerate((Tk, Tk, Toplevel,)):
    win = cls()
    win.title(cls.__name__ + str(ix))
    Button(win, text='quit   ', command=win.quit).pack()
    Button(win, text='destroy', command=win.destroy).pack()
    b = Button(win, text='selfquit')
    b.config(command=b.quit)
    b.pack()
    b = Button(win, text='selfdestroy')
    b.config(command=b.destroy)
    b.pack()
    Button(text='where?').pack()

mainloop()

