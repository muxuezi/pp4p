"add a label on the top and form resizing"

from tkinter import *
colors = ['red',  'white',  'blue']

def gridbox(root):
    Label(root, text='Grid').grid(columnspan=2)
    row = 1
    for color in colors:
        lab = Label(root, text=color, relief=RIDGE,  width=25)
        ent = Entry(root, bg=color,   relief=SUNKEN, width=50)
        lab.grid(row=row, column=0, sticky=NSEW)
        ent.grid(row=row, column=1, sticky=NSEW)
        root.rowconfigure(row, weight=1)
        row += 1
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

def packbox(root):
    Label(root, text='Pack').pack()
    for color in colors:
        row = Frame(root)
        lab = Label(row, text=color, relief=RIDGE,  width=25)
        ent = Entry(row, bg=color,   relief=SUNKEN, width=50)
        row.pack(side=TOP,   expand=YES, fill=BOTH)
        lab.pack(side=LEFT,  expand=YES, fill=BOTH)
        ent.pack(side=RIGHT, expand=YES, fill=BOTH)

root = Tk()
gridbox(Toplevel(root))
packbox(Toplevel(root))
Button(root, text='Quit', command=root.quit).pack()
mainloop()
