# customize to erase or show button on after() timer callbacks

from tkinter import *
import alarm

class Alarm(alarm.Alarm):                        # change alarm callback
    def __init__(self, msecs=1000):              # default = 1 second
        self.shown = False
        alarm.Alarm.__init__(self, msecs)

    def repeater(self):                          # on every N millisecs
        self.bell()                              # beep now
        if self.shown:
            self.stopper.pack_forget()           # hide or erase button now
        else:                                    # or reverse colors, flash...
            self.stopper.pack()
        self.shown = not self.shown              # toggle state for next time
        self.after(self.msecs, self.repeater)    # reschedule handler

if __name__ == '__main__': Alarm(msecs=500).mainloop()
