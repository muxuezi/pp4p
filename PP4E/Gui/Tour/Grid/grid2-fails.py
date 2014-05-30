"""
FAILS-- can't grid and pack in same parent container (here, root window)
"""

from tkinter import *
from grid2 import gridbox, packbox

root = Tk()
gridbox(root)
packbox(root)
Button(root, text='Quit', command=root.quit).pack()
mainloop()
