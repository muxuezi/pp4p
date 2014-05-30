from tkinter import *

def handler(A, B):
    print(A, B)

def makegui():
    X = 42
    Button(text='ni', command=(lambda: handler(X, 'spam'))).pack()   # remembers X

makegui()
mainloop()
