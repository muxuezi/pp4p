from menu_win import makemenu       # reuse menu maker function
from tkinter import *

root = Tk()
for i in range(3):                  # three pop-up windows with menus
    win = Toplevel(root)
    makemenu(win)
    Label(win, bg='black', height=5, width=25).pack(expand=YES, fill=BOTH)
Button(root, text="Bye", command=root.quit).pack()
root.mainloop()
