import sys
from tkinter import *                        # lambda generates a function

widget = Button(None,                        # but contains just an expression
             text='Hello event world',
             command=(lambda: print('Hello lambda world') or sys.exit()) )

widget.pack()
widget.mainloop()
