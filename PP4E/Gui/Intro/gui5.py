from tkinter import *

class HelloButton(Button):
    def __init__(self, parent=None, **config):         # add callback method
        Button.__init__(self, parent, **config)        # and pack myself
        self.pack()                                    # could config style too
        self.config(command=self.callback)

    def callback(self):                                # default press action
        print('Goodbye world...')                      # replace in subclasses
        self.quit()

if __name__ == '__main__':
    HelloButton(text='Hello subclass world').mainloop()

