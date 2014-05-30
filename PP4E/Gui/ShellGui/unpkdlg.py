# popup a GUI dialog for unpacker script arguments, and run it

from tkinter import *                             # widget classes
from unpacker import unpack                       # use unpack script/module
from formrows import makeFormRow                  # form fields builder

def unpackDialog():                   
    win = Toplevel()
    win.title('Enter Unpack Parameters')
    var = makeFormRow(win, label='Input file', width=11)
    win.bind('<Key-Return>', lambda event: win.destroy())
    win.grab_set()
    win.focus_set()                  # make myself modal
    win.wait_window()                # till I'm destroyed on return
    return var.get()                 # or closed by wm action

def runUnpackDialog():
    input = unpackDialog()                    # get input from GUI
    if input != '':                           # do non-GUI file stuff
        print('Unpacker:', input)             # run with input from dialog
        unpack(ifile=input, prefix='')

if __name__ == "__main__":
    Button(None, text='popup', command=runUnpackDialog).pack()
    mainloop()
