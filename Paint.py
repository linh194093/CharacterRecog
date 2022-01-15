from tkinter import *
import tkinter
from tkinter.ttk import Scale
from tkinter import colorchooser, messagebox
from tkinter.filedialog import asksaveasfilename
from PIL.Image import new
import PIL.ImageGrab as ImageGrab 
import numpy as np
import Detection.Main_detection as detect
import cv2
import Word_recognize.predict_array as RecogA
import tensorflow as tf
from PIL import ImageTk, Image  
import time

color = 'white'
i = 1
Picture = np.array([])
new_model = tf.keras.models.load_model('Word_recognize/model_and_weight_12_12/model_.h5')
new_model.load_weights("Word_recognize/model_and_weight_12_12/model_weights_.h5")
new_model2 = tf.keras.models.load_model('Word_recognize/model1/model.h5')
new_model2.load_weights("Word_recognize/model1/model_weights.h5")

text1 = ""
text2 = ""

class Paint:

    def __init__(self, root):
        self.root = root
        self.root.title('Paint')
        self.root.geometry("{0}x{1}+0+0".format(1380, 710))
        #self.root.geometry("{0}x{1}+0+0".format(1400, 700))
        self.root.configure(background= 'pink')

        # self.root.resizable(0, 0)
        

        self.pen_color = '#000000'

        self.color_frame = LabelFrame(
            self.root,
            text='Color',
            font=('arial', 15, 'bold'),
            bd=5,
            relief=RIDGE,
            bg='pink',
            )
        self.color_frame.place(x=10, y=0, width=160, height=110)

        Colors = [
            '#000000',
            '#333333',
            '#555555',
            '#FFFFFF',
            '#EE0000',
            '#FF3300',
            '#FFFF00',
            '#FF99FF',
            '#0000FF',
            '#3366CC',
            '#00FF00',
            '#CC99FF',
            ]
        i = j = 0
        for color in Colors:

            Button(
                self.color_frame,
                bg=color,
                command=lambda col=color: self.select_color(col),
                width=4,
                bd=2,
                relief=RIDGE,
                ).grid(row=i, column=j)
            j += 1
            if j == 4: 
                if i == 0:
                    i = 1
                    j = 0
                else:
                    i = 2
                    j = 0


        self.erase_button = Button(
            self.root,
            text='Eraser',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.eraser,
            bg='#33CCFF',
            
            )
        self.erase_button.place(x=10, y=113)

        self.clear_sreen_button = Button(
            self.root,
            text='Clear',
            bd=4,
            relief=RIDGE,
            width=21,
            command=lambda : self.canvas.delete('all'),
            bg='#33CCFF',
            )
        self.clear_sreen_button.place(x=10, y=137)

        self.save_button = Button(
            self.root,
            text='Save',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.save_paint,
            bg='#33CCFF',
            
            )
        self.save_button.place(x=10, y=167)

        self.canvas_color_button = Button(
            self.root,
            text='Canvas',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.canvas_color,
            bg='#33CCFF',
            
            )
        self.canvas_color_button.place(x=10, y=197)

        self.pen_size_scale_frame = LabelFrame(
            self.root,
            text='Size',
            bd=5,
            relief=RIDGE,
            bg='pink',
            font=('arial', 15, 'bold'),
            )
        self.pen_size_scale_frame.place(x=55, y=230, height=200,
                width=70)

        self.pen_size = Scale(
            self.pen_size_scale_frame,
            orient='vertical',
            from_=40,
            to=0,
            command=None,
            length=170,
            )
        self.pen_size.set(10)
        self.pen_size.grid(row=0, column=1, padx=15)

# Dự đoán theo mô hình 1
        self.predict_button1 = Button(
            self.root,
            text='predict1',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.predict_method1,
            bg='#33CCFF',
            activebackground='#4444ff',
            
            )
        self.predict_button1.place(x=10, y=435)
# Dự đoán theo mô hình 2
        self.predict_button2 = Button(
            self.root,
            text='predict2',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.predict_method2,
            bg='#33CCFF',
            activebackground='#4444ff',
            
            )
        self.predict_button2.place(x=10, y=465)

        self.predict_button3 = Button(
            self.root,
            text='Show detail',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.show_detail,
            bg='#33CCFF',
            activebackground='#4444ff',
            
            )
        self.predict_button3.place(x=10, y=495)

        self.pre_run = Button(
            self.root,
            text='Pre-run',
            bd=4,
            relief=RIDGE,
            width=21,
            command=self.pre_run,
            bg='#33CCFF',
            activebackground='#4444ff',
            
            )
        self.pre_run.place(x=10, y=525)

        self.canvas = Canvas(
            self.root,
            bg='white',
            bd=5,
            relief='groove',
            height=500,
            width=1160,
            
            )
        self.canvas.place(x=180, y=180)

        self.canvas1 = Text(
            self.root,
            bg='#99FFFF',
            font =("Verdana", 31),
            bd=5,
            height=3.0,
            width=31
            )
        self.canvas1.place(x=180, y=10)
        self.canvas1.insert(tkinter.END, "Project by Group 10")

        self.canvas2 = Text(
            self.root,
            bg='#99FFFF',
            font =("Verdana", 31),
            bd=5,
            height=3.0,
            width=13
            )
        self.canvas2.place(x=1005, y=10)
        self.canvas2.insert(tkinter.END, "Predict: ")
        # self.canvas1.create_text(100,20,fill="darkblue",font="Times 20 italic bold",text="A")

        # Blind mouse dragging event to canvas

        self.canvas.bind('<B1-Motion>', self.paint)
        self.old_x = None
        self.old_y = None
        self.canvas.bind('<ButtonRelease-1>', self.reset)


    def paint(self, event):
        global pen_color
        if self.old_x and self.old_y:

            self.canvas.create_line(
                self.old_x,
                self.old_y,
                event.x,
                event.y,
                width=self.pen_size.get(),
                fill=self.pen_color,
                capstyle=ROUND,
                smooth=TRUE,
                splinesteps=36,
                )

        self.old_x = event.x
        self.old_y = event.y

    def reset(self,*args):
        self.old_x = None
        self.old_y = None

    def select_color(self, col):
        global i
        i = 1
        self.pen_color = col

    def eraser(self):
        global color
        global i
        self.pen_color = color
        # self.canvas.config(cursor='dot')
        i = 0

    def canvas_color(self):
        global color
        color = colorchooser.askcolor()
        color = color[1]
        self.canvas.config(background=color)

    def save_paint(self):
        try:
            self.canvas.update()
            filename = asksaveasfilename(defaultextension='.jpg')
            print("File được lưu tại: " + filename)
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            w = x + self.canvas.winfo_width()
            h = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, w, h)).save(filename)
            messagebox.showinfo('paint says ', 'image is saved as '
                                + str(filename))
        except:
            print("Un exported")
            pass

    def predict_method1(self):
        global Picture
        global text1
        # self.canvas1.delete('1.0', tkinter.END)

        global new_model
        
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()

        Picture = np.array(ImageGrab.grab().crop((x, y, w, h)))
        Result = detect.take_from_array([Picture])


        List_image = []
        for crop_image in Result:
            List_image.append(crop_image)
        KQ = RecogA.predict_array(List_image, new_model)
        KQ.FResult
        self.canvas1.insert(tkinter.END, KQ.FResult)
        self.canvas2.delete('1.0', tkinter.END)
        self.canvas2.insert(tkinter.END, KQ.FResult)
        pass

    def predict_method2(self):
        global Picture
        global text2
        # self.canvas1.delete('1.0', tkinter.END)

        global new_model
        
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        Picture = np.array(ImageGrab.grab().crop((x, y, w, h)))
        time1 = time.time()
        Result = detect.take_from_array([Picture])

        List_image = []
        for crop_image in Result:
            List_image.append(crop_image)
        KQ = RecogA.predict_array(List_image, new_model2)
        
        KQ.FResult
        print("time: ")
        print(time.time() - time1)
        self.canvas1.insert(tkinter.END, KQ.FResult)
        self.canvas2.delete('1.0', tkinter.END)
        self.canvas2.insert(tkinter.END, KQ.FResult)
        pass

    def show_detail(self):
        global Picture
        global text2
        # self.canvas1.delete('1.0', tkinter.END)

        global new_model
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        Picture = np.array(ImageGrab.grab().crop((x, y, w, h)))
        Result = detect.take_from_array([Picture], show_detail = 1)

        List_image = []
        for crop_image in Result:
            List_image.append(crop_image)
        KQ = RecogA.predict_array(List_image, new_model2)
        self.canvas1.insert(tkinter.END, KQ.FResult)
        self.canvas2.delete('1.0', tkinter.END)
        self.canvas2.insert(tkinter.END, KQ.predict)       
        
        pass

    def pre_run(self):
        global Picture
        global text2
        # self.canvas1.delete('1.0', tkinter.END)

        global new_model
        
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        Picture = np.array(ImageGrab.grab().crop((x, y, w, h)))
        Result = detect.take_from_array([Picture])

        List_image = []
        for crop_image in Result:
            List_image.append(crop_image)
        KQ = RecogA.predict_array(List_image, new_model2)
        KQ.FResult
        self.canvas1.delete('1.0', tkinter.END)
        self.canvas2.delete('1.0', tkinter.END)
        pass
