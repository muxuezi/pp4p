# flash and beep every second using after() callback loop

from tkinter import *

class Alarm(Frame):
    def __init__(self, msecs=1000):              # default = 1 second
        Frame.__init__(self)
        self.msecs = msecs
        self.pack()
        stopper = Button(self, text='Stop the beeps!', command=self.quit)
        stopper.pack()
        stopper.config(bg='navy', fg='white', bd=8)
        self.stopper = stopper
        self.repeater()

    def repeater(self):                          # on every N millisecs
        self.bell()                              # beep now
        self.stopper.flash()                     # flash button now
        self.after(self.msecs, self.repeater)    # reschedule handler

if __name__ == '__main__': Alarm(msecs=1000).mainloop()
