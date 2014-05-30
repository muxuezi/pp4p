from tkinter import *
imgdir = '.\\'
main = Tk()

from PIL import Image, ImageTk
imageobj = Image.open(imgdir + "ora-lp4e.jpg")
photoimg = ImageTk.PhotoImage(imageobj)
Button(image=photoimg).pack()


mainloop()
