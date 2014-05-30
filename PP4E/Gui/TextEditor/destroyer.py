# simulate effect of a bound <Destroy> event in PyEdit: can't access GUI in handler!
# uncomment lines in callback handlers here to experiment with this on your machine

from tkinter import *
from tkinter.messagebox import askyesno

def onDeleteRequest():
    print('Got wm delete')
    root.destroy()                  # destroys root and all children, triggers <Destroy>

def doRootDestroy(event):
    print('Got event <destroy>')    # called 4 times: for each widget
    if event.widget == text:
        print('for text')
        #print(text.edit_modified())                # <= Tcl error: invalid widget
        #ans = askyesno('Save stuff?', 'Save?')     # <= may behave badly
        #if ans: print(text.get('1.0', END+'-1c'))  # <= Tcl error: invalid widget

def doTextDestroy(event):
    print('Got text <destroy>')
    #print(text.edit_modified())                # <= Tcl error: invalid widget
    #ans = askyesno('Save stuff?', 'Save?')     # <= may behave badly
    #if ans: print(text.get('1.0', END+'-1c'))  # <= Tcl error: invalid widget

root = Tk()
text = Text(root, undo=1, autoseparators=1)
text.pack()

# try one or the other (or both)...
root.bind('<Destroy>', doRootDestroy)     # for root and all children (case matters!)
#text.bind('<Destroy>', doTextDestroy)    # just for the text object

root.protocol('WM_DELETE_WINDOW', onDeleteRequest)
Button(root, text='Destroy', command=root.destroy).pack()
Button(root, text='Quit',    command=root.quit).pack()     # <= fatal Python error, no <Destroy> run

mainloop()
print('After mainloop')   # here after all widgets closed
