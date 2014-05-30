"""
This is original peoplegui.py from the prior edition (with a few minor updates);
because it used pack() + nested side frames, labels didn't align with entries 
quite correctly on Windows 7, and may have been even further askew elsewhere;
run this and persongui.py to see the difference--on Windows 7, the first and 
last field labels are slightly too high and low, respectively; to do better, 
this was changed to use grid() instead of pack(), and most form-like examples 
in the book probably should as well; the PyMailGui example aleady was already
so updated in a later release of the prior edition's example package.

See also peoplegui--frame.py here for an alternative way to layout forms with
pack() using nested row frames and fixed-width labels, that looks just as nice
as grid(), and is roughly the same in terms of code size.  The version here,
though, relies on font size and layout algorithms to align at all.
"""

from tkinter import *
from tkinter.messagebox import showerror
import shelve
shelvename = 'class-shelve'
fieldnames = ('name', 'age', 'job', 'pay')

def makeWidgets():
    global entries
    window = Tk()
    window.title('People Shelve')
    form   = Frame(window)
    labels = Frame(form)
    values = Frame(form)
    labels.pack(side=LEFT)
    values.pack(side=RIGHT)
    form.pack()
    entries = {}
    for label in ('key',) + fieldnames:
        Label(labels, text=label).pack()
        ent = Entry(values)
        ent.pack()
        entries[label] = ent
    Button(window, text="Fetch",  command=fetchRecord).pack(side=LEFT)
    Button(window, text="Update", command=updateRecord).pack(side=LEFT)
    Button(window, text="Quit",   command=window.quit).pack(side=RIGHT)
    return window

def fetchRecord():
    key = entries['key'].get()
    try:
        record = db[key]                      # fetch by key, show in GUI
    except:
        showerror(title='Error', message='No such key!')
    else:
        for field in fieldnames:
            entries[field].delete(0, END)
            entries[field].insert(0, repr(getattr(record, field)))

def updateRecord():
    key = entries['key'].get()
    if key in db:
        record = db[key]                      # update existing record
    else:
        from person import Person             # make/store new one for key
        record = Person(name='?', age='?')    # eval: strings must be quoted
    for field in fieldnames:
        setattr(record, field, eval(entries[field].get()))
    db[key] = record

db = shelve.open(shelvename)
window = makeWidgets()
window.mainloop()
db.close() # back here after quit or window close
