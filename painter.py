#!/usr/bin/python
#painter.py
__author__ = "Elijah"
__version__ = 2.0

import tkinter as tk
from PIL import Image, ImageGrab

class Draw_tools(object):
    pen_size = 1.0

    def __init__(self, bg, canvas, color, circle_creator, erased, line_creator,
                 moves, root, sizer, square_creator, pen_size_slider, slider):
        """Sets up all the drawing tools

        :param bg: the current background
        :param canvas: the drawing canvas
        :param color: the current brush color
        :param circle_creator: whether or not circle mode is on
        :param erased: the list of erased lines
        :param line_creator: whether or not line mode is on
        :param moves: the list of total moves
        :param root: the tkinter window
        :param sizer: whether or not the pen size slider is open
        :param pen_size_slider: the slider for the size of the pen
        :param slider: the circle that shows the current brush size
        :return: None"""
        
        self.root = root
        self.pen_button    = tk.Button(self.root, text="pen", command=self.set_pen_mode)
        self.eraser_button = tk.Button(self.root, text="eraser", command=self.set_eraser_mode)
        self.save_button   = tk.Button(self.root, text="save", command=self.save)
        self.submit_btn    = tk.Button(self.root, text="submit", command=self.submit)
        
        self.entry = tk.Entry(self.root, bd=5)
        self.box   = tk.Listbox(self.root, height=2, width=5)
        
        self.bg             = bg
        self.color          = color
        self.circle_creator = circle_creator
        self.erased         = erased
        self.line_creator   = line_creator
        self.moves          = moves
        self.slider         = slider
        self.square_creator = square_creator
        
        self.sizer           = sizer
        self.pen_size_slider = pen_size_slider
        self.canvas          = canvas

        self.pen_button.grid(row=0, column=7)
        self.eraser_button.grid(row=0, column=8)
        self.save_button.grid(row=0, column=9)
        
        self.file_name = ""
        self.file_type = ""
        
        self.moving = []
        
        self.draw_mode  = False
        self.master     = None
        
        self.setup()

    def setup(self):
        """Setups all the variables for the class"""
        
        self.old_x = None
        self.old_y = None
        self.line_width = self.pen_size_slider.get()
        self.eraser_on = False
        self.active_button = self.pen_button
        
        #listens for mouse clicks and movement
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.root.bind("<Command-s>", lambda x: self.save())

    def set_pen_mode(self):
        """Turns on pen mode and sets the cursor to a pencil"""
        
        self.activate_button(self.pen_button)
        self.draw_mode = True
        self.canvas.config(cursor="pencil")

    def set_eraser_mode(self):
        """Turns on eraser mode"""
        
        self.draw_mode = True
        self.activate_button(self.eraser_button, eraser_mode=True)

    def save(self):
        """Saves the file with the user's choice of file name"""
        
        self.entry.grid(row=1, column=9, rowspan=1, columnspan=1)
        self.box.grid(row=1, column=10, rowspan=1, columnspan=1)
        self.submit_btn.grid(row=0, column=9, rowspan=1, columnspan=1)
        
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
        self.x1 = self.root.winfo_x() + self.canvas.winfo_x() + x_dist
        self.y1 = self.root.winfo_y() + self.canvas.winfo_y() + y_dist
        self.x2 = self.x1 + self.canvas.winfo_width() - x_dist * 2
        self.y2 = self.y1 + self.canvas.winfo_height() - y_dist -(x_dist * 2)
        
        #checks if a file might be overwritten
        try:
            img = Image.open(self.file_name + file_type)
            
            self.master = tk.Tk()
            label = tk.Label(self.master, text="WARNING!\nYou already have a "+\
                               "file with this name. Do you want to overwrite it?")
            yes_button = tk.Button(self.master, text="Yes", command=self.continue_saving)
            no_button  = tk.Button(self.master, text="No", command=self.stop_saving)
            
            label.pack()
            yes_button.pack()
            no_button.pack()
        
        except FileNotFoundError:
            self.continue_saving()

    def continue_saving(self):
        """Continues saving the file"""
        
        if self.master != None:
            self.master.destroy()
            
        #takes a screenshot, crops the window, and saves
        ImageGrab.grab().crop((self.x1, self.y1, self.x2, self.y2)).save(self.file_name
                                                                         + self.file_type)
    
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
        
        #removes the slider from the window
        if self.sizer:
            self.pen_size_slider.grid_forget()
            self.canvas.delete(self.slider)
            
            self.slider = None
            self.sizer  = False
        
        if (self.circle_creator or self.line_creator or self.square_creator) and not self.draw_mode:
            return False
        
        self.canvas.config(cursor="pencil")
        
        #sets the color of the brush
        if self.color != "":
            self.color = self.color
        else:
            self.color = "black"
            
        self.line_width = self.pen_size_slider.get()
        
        #activates eraser if eraser mode is on
        if self.eraser_on:
            self.canvas.config(cursor="")
            if self.bg != "":
                paint_color = self.bg
            else:
                paint_color = "white"
        else:
            paint_color = self.color
        
        #connects the line to the mouse
        if self.old_x and self.old_y:
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
