from tkinter import *
Label(None, {'text': 'Hello GUI world!', Pack: {'side': 'top'}}).mainloop()


"""
from tkinter import *
options = {'text': 'Hello GUI world!'}
layout  = {'side': 'top'}
Label(None, **options).pack(**layout)        # keyword must be strings
mainloop()
"""