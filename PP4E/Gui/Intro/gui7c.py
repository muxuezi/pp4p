import gui7
from tkinter import *

class HelloPackage(gui7.HelloPackage):
    def __getattr__(self, name):
        return getattr(self.top, name)                  # pass off to a real widget

if __name__ == '__main__': HelloPackage().mainloop()    # invokes __getattr__
