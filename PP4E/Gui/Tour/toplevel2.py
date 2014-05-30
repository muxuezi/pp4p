"""
pop up three new windows, with style
destroy() kills one window, quit() kills all windows and app (ends mainloop);
top-level windows have title, icon, iconify/deiconify and protocol for wm events;
there always is an application root window, whether by default or created as an
explicit Tk() object; all top-level windows are containers, but they are never
packed/gridded; Toplevel is like Frame, but a new window, and can have a menu;
"""

from tkinter import *
root = Tk()                                                     # explicit root

trees = [('The Larch!',         'light blue'),
         ('The Pine!',          'light green'),
         ('The Giant Redwood!', 'red')]

for (tree, color) in trees:
    win = Toplevel(root)                                        # new window
    win.title('Sing...')                                        # set border
    win.protocol('WM_DELETE_WINDOW', lambda:None)               # ignore close
    win.iconbitmap('py-blue-trans-out.ico')                     # not red Tk

    msg = Button(win, text=tree, command=win.destroy)           # kills one win
    msg.pack(expand=YES, fill=BOTH)
    msg.config(padx=10, pady=10, bd=10, relief=RAISED)
    msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))

root.title('Lumberjack demo')
Label(root, text='Main window', width=30).pack()
Button(root, text='Quit All', command=root.quit).pack()         # kills all app
root.mainloop()
