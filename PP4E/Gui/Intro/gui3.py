import sys
from tkinter import *

def quit():                                  # a custom callback handler
    print('Hello, I must be going...')       # kill windows and process
    sys.exit()

widget = Button(None, text='Hello event world', command=quit)
widget.pack()
widget.mainloop()

