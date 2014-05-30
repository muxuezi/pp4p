from menu_frm import makemenu         # can't use menu_win here--root=Frame
from tkinter import *

root = Tk()
for i in range(3):                    # three menus nested in the containers
    frm = Frame()
    mnu = makemenu(frm)
    mnu.config(bd=2, relief=RAISED)
    frm.pack(expand=YES, fill=BOTH)
    Label(frm, bg='black', height=5, width=25).pack(expand=YES, fill=BOTH)
Button(root, text="Bye", command=root.quit).pack()
root.mainloop()
