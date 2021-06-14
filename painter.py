#!/usr/bin/python
#painter.py
__author__ = "Elijah"
__version__ = 2.4

import tkinter as tk
from PIL import Image, ImageGrab
import math

class Draw_tools(object):
    pen_size = 1.0

    def __init__(self, bg, canvas, color, circle_creator, erased, fill_mode,
                 height, line_creator, moves, root, square_creator,
                 pen_size_slider, slider, width, x_shift, y_shift):
        """Sets up all the drawing tools

        :param bg: the current background
        :param canvas: the drawing canvas
        :param color: the current brush color
        :param circle_creator: whether or not circle mode is on
        :param erased: the list of erased lines
        :param fill_mode: whether or not fill mode is on
        :param height: the height of the window
        :param line_creator: whether or not line mode is on
        :param moves: the list of total moves
        :param root: the tkinter window
        :param square_creator: whether or not square mode is on
        :param pen_size_slider: the slider for the size of the pen
        :param slider: the circle that shows the current brush size
        :param width: the width of the window
        :param x_shift: the amount the window is shifted horizontally
        :param y_shift: the amount the window is shifted vertically
        :return: None"""
        
        self.root = root
        self.pen_img    = tk.PhotoImage(file="Tkinter_Images/pencil.gif")
        self.eraser_img = tk.PhotoImage(file="Tkinter_Images/eraser.gif")
        self.brush_img  = tk.PhotoImage(file="Tkinter_Images/brush.gif")
        
        self.pen_button    = tk.Button(self.root, image=self.pen_img, command=self.set_pen_mode)
        self.brush_button  = tk.Button(self.root, image=self.brush_img, command=self.set_brush_mode)
        self.eraser_button = tk.Button(self.root, image=self.eraser_img, command=self.set_eraser_mode)
        self.save_button   = tk.Button(self.root, text="save", command=self.save)
        self.submit_btn    = tk.Button(self.root, text="submit", command=self.submit)
        
        self.entry = tk.Entry(self.root, bd=5)
        self.box   = tk.Listbox(self.root, height=2, width=5)
        
        self.bg             = bg
        self.color          = color
        self.circle_creator = circle_creator
        self.erased         = erased
        self.fill_mode      = fill_mode
        self.height         = height - 60
        self.line_creator   = line_creator
        self.moves          = moves
        self.slider         = slider
        self.square_creator = square_creator
        self.width          = width - 35
        self.x_shift        = x_shift
        self.y_shift        = y_shift
        
        self.pen_size_slider = pen_size_slider
        self.canvas          = canvas
        
        self.save_button.grid(row=10, column=0)
        self.pen_button.grid(row=11, column=0)
        self.brush_button.grid(row=12, column=0)
        self.eraser_button.grid(row=13, column=0)
        
        self.file_name = ""
        self.file_type = ""
        
        self.moving = []
        
        self.draw_mode  = False
        self.brush_mode = False
        self.master     = None
        
        self.setup()

    def setup(self):
        """Setups all the variables for the class"""
        
        self.old_x = None
        self.old_y = None
        self.line_width = self.pen_size
        self.eraser_on = False
        self.active_button = self.pen_button
        
        #listens for mouse clicks and movement
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.root.bind("<Command-s>", lambda x: self.save())

    def set_pen_mode(self):
        """Turns on pen mode and sets the cursor to a pencil"""
        
        self.activate_button(self.pen_button)
        self.draw_mode  = True
        self.brush_mode = False
        self.canvas.config(cursor="@Tkinter_Images/pencil.cur")
    
    def set_brush_mode(self):
        """Turns on brush mode and sets cursor to a brush"""
        
        self.activate_button(self.brush_button)
        self.canvas.config(cursor="@Tkinter_Images/brush.cur")
        self.draw_mode  = True
        self.brush_mode = True

    def set_eraser_mode(self):
        """Turns on eraser mode"""
        
        self.draw_mode  = True
        self.brush_mode = False
        self.activate_button(self.eraser_button, eraser_mode=True)
        self.canvas.config(cursor="@Tkinter_Images/eraser.cur")

    def save(self):
        """Saves the file with the user's choice of file name"""
        
        self.entry.grid(row=10, column=2, rowspan=1, columnspan=1)
        self.box.grid(row=11, column=2, rowspan=1, columnspan=1)
        self.submit_btn.grid(row=10, column=1, rowspan=1, columnspan=1)
        
        self.box.insert(0, 'GIF')
        self.box.insert(1, 'PNG')
    
    def submit(self):
        """Gets file name that the user chose and saves the image

        :return: True if user doesn't want to overwrite the file,
                 False if no given file name or file choice"""
        
        file_name = self.entry.get()
        file_choice = self.box.curselection()
        
        if len(file_name) == 0:
            return False
        
        #determines the type of the file (.gif or .png)
        if 0 in file_choice:
            file_type = '.gif'
        elif 1 in file_choice:
            file_type = '.png'
        else:
            return False
        
        self.file_name = "Images/" + file_name
        self.file_type = file_type
        
        self.entry.grid_forget()
        self.box.grid_forget()
        self.submit_btn.grid_forget()
        
        x_dist = 5
        y_dist = 30
        
        #gets the size of the window
        self.x1 = self.x_shift
        self.y1 = self.y_shift
        self.x2 = 2000
        self.y2 = 1500
        
        #checks if a file might be overwritten
        try:
            img = Image.open(self.file_name + file_type)
            
            self.master = tk.Tk()
            self.master.title("")
            label = tk.Label(self.master, text="WARNING!\nYou already have a "+\
                               "file with this name. Do you want to overwrite it?")
            yes_button = tk.Button(self.master, text="Yes", command=self.continue_saving)
            no_button  = tk.Button(self.master, text="No", command=self.stop_saving)
            
            label.pack()
            yes_button.pack()
            no_button.pack()
        
        except FileNotFoundError:
            self.continue_saving()
        
        except:
            self.continue_saving()

    def continue_saving(self):
        """Continues saving the file"""
        
        if self.master != None:
            self.master.destroy()
            
        #takes a screenshot, crops the window, and saves
        self.canvas.postscript(file=self.file_name + '.eps')
        
        #.grab().crop((self.x1, self.y1, self.x2, self.y2)).save(self.file_name
                                                                         #+ self.file_type)
    
    def stop_saving(self):
        """Stops saving the file"""
        self.master.destroy()
        

    def activate_button(self, button, eraser_mode=False):
        """Activates the current button

        :param button: the active button
        :param eraser_mode: whether or not eraser mode is on
        :return: None"""
        
        #turns off circle, line, and square mode
        self.line_creator   = False
        self.circle_creator = False
        self.square_creator = False
        
        #sets the currently active button
        self.active_button.config(relief = "raised")
        button.config(relief = "sunken")
        self.active_button = button
        self.eraser_on     = eraser_mode

    def paint(self, event):
        """Draws a line following the mouse

        :param event: the last place where the mouse was
        :return: False if circle mode or line mode is active"""
        
        if (self.circle_creator or self.line_creator or self.square_creator
            or self.fill_mode) and not self.draw_mode:
            return False
        
        
        #sets the color of the brush
        if self.color != "":
            self.color = self.color
        else:
            self.color = "black"
        
        try:
            self.line_width = self.pen_size_slider.get()
        except AttributeError:
            pass
        
        #activates eraser if eraser mode is on
        if self.eraser_on:
            self.canvas.config(cursor="@Tkinter_Images/eraser.cur")
            if self.bg != "":
                paint_color = self.bg
            else:
                paint_color = "white"
        else:
            paint_color = self.color
            if self.brush_mode:
                self.canvas.config(cursor="@Tkinter_Images/brush.cur")
            else:
                self.canvas.config(cursor="@Tkinter_Images/pencil.cur")
        
        
        #connects the line to the mouse
        if self.old_x and self.old_y:
            if self.brush_mode:
                x = abs((event.x ** 2) - (self.old_x ** 2))
                y = abs((event.y ** 2) - (self.old_y ** 2))
                x = round(math.sqrt(x), 3)
                y = round(math.sqrt(y), 3)
                dist = (x + y) // 2
                width = abs(dist - self.line_width) % self.line_width
                
                
                line = self.canvas.create_line(self.old_x, self.old_y, event.x,
                                               event.y, width=width,
                                               fill=paint_color, capstyle='round',
                                               smooth='true', joinstyle='miter',
                                               dash=(2, 1,))
            else:
                line = self.canvas.create_line(self.old_x, self.old_y, event.x,
                                               event.y, width=self.line_width,
                                               fill=paint_color, capstyle='round',
                                               smooth='true', splinesteps=36)
            if self.eraser_on:
                self.erased.append(line)
            self.moving.append(line)
        
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        """Resets the variables after the mouse lets go

        :param event: the place where the mouse let go
        :return: None"""
        
        if len(self.moving) != 0:
            self.moves.append(self.moving)
            self.moving = []
        
        self.old_x = None
        self.old_y = None
