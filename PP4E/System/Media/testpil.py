from tkinter import * 

# GIF works, but JPEG requires PIL
imgfile1 = 'ora-pp3e.gif'
imgfile2 = 'ora-lp4e.jpg'

win = Tk()    # make root first
win.title('%s and %s' % (imgfile1, imgfile2))

imgobj1 = PhotoImage(file=imgfile1)       # display standard photo on a Label
Label(win, image=imgobj1).pack()
print(imgobj1.width(), imgobj1.height())  # show size in pixels before destroyed

from PIL.ImageTk import PhotoImage
imgobj2 = PhotoImage(file=imgfile2)       # display PIL photo on a Label
Label(win, image=imgobj2).pack()
print(imgobj2.width(), imgobj2.height())  # show size in pixels before destroyed

win.mainloop()