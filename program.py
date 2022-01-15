from tkinter import *


def raise_frame(frame):
    frame.tkraise()
import Paint
from tkinter import *



# root = Tk()
# f1 = Frame(root)


# f1.grid(row=0, column=0, sticky='news')

# Button(f1, text='Go to frame 2', command=lambda:Paint.Paint(root)).pack()
# Label(f1, text='FRAME 1').pack()


# raise_frame(f1)
# root.mainloop()


from tkinter import *
from PIL import ImageTk, Image
import os
 
root = Tk()

img = ImageTk.PhotoImage(Image.open("istockphoto-1262838212-170667a.jpg"))

Button(root, text='Go to frame 2', command=lambda:Paint.Paint(root)).pack()

panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
panel.configure(background='pink')
root.configure(background= 'pink')
root.mainloop()

