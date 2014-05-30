# popup a GUI dialog for packer script arguments, and run it

from glob import glob                           # filename expansion
from tkinter import *                           # GUI widget stuff
from packer import pack                         # use pack script/module
from formrows import makeFormRow                # use form builder tool

def packDialog():                               # a new top-level window
    win = Toplevel()                            # with 2 row frames + ok button
    win.title('Enter Pack Parameters')
    var1 = makeFormRow(win, label='Output file')
    var2 = makeFormRow(win, label='Files to pack', extend=True) 
    Button(win, text='OK', command=win.destroy).pack()
    win.grab_set()                   
    win.focus_set()                  # go modal: mouse grab, keyboard focus, wait
    win.wait_window()                # wait till destroy; else returns now
    return var1.get(), var2.get()    # fetch linked var values

def runPackDialog():
    output, patterns = packDialog()                  # pop-up GUI dialog
    if output != "" and patterns != "":              # till ok or wm-destroy
        patterns = patterns.split()                  # do non-GUI part now
        filenames = []
        for sublist in map(glob, patterns):          # do expansion manually
            filenames += sublist                     # Unix shells do this auto
        print('Packer:', output, filenames)
        pack(ofile=output, ifiles=filenames)         # should show msgs in GUI too

if __name__ == '__main__':
    root = Tk()
    Button(root, text='popup', command=runPackDialog).pack(fill=X)
    Button(root, text='bye',   command=root.quit).pack(fill=X)
    root.mainloop()
