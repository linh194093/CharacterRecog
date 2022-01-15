import Paint
from tkinter import *
import time


if __name__ == '__main__':
    t = time.time()
    root = Tk()
    Paint.Paint(root)
    print(time.time() - t)
    root.mainloop()



