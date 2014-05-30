"""
FAILS-- can't grid and pack in same parent container (here, root window)
"""

from tkinter import *
from grid2 import gridbox, packbox

root = Tk()
frm = Frame(root)
frm.pack()            # this works
gridbox(frm)          # gridbox must have its own parent in which to grid
packbox(root)
Button(root, text='Quit', command=root.quit).pack()
mainloop()

