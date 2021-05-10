#!/usr/bin/python
#animation_runner.py
__author__ = "Elijah"
__version = 2.7

import tkinter as tk
from tkinter import colorchooser

height  = 500
width   = 900
x_shift = 0
y_shift = 20

slider  = None

bg = "white"

circle_creator = False
line_creator   = False

coords  = []
circles = []
erased  = []
lines   = []
moves   = []

root = tk.Tk()
root.title("Animation")

def colors():
    global color
    current_color = colorchooser.askcolor(title="Choose color")
    color = current_color[1]

def slider_circle(event):
    global size_slider, canvas, width, height, slider
    
    amt = size_slider.get()
    amt //= 2
    
    height_pos = height // 2
    width_pos  = width // 2
    
    canvas.delete(slider)
    coords = [width_pos - amt, height_pos - amt, width_pos + amt, height_pos + amt]
    slider = canvas.create_oval(coords, fill="white", outline="black")

canvas = tk.Canvas(root, width=width, height=height, bg=bg)
color_button = tk.Button(root, text="Color", command=colors)
size_slider = tk.Scale(root, from_=1, to=30, orient="horizontal", command=slider_circle)
color = ""

def options():
    undo_button       = tk.Button(root, text="Undo", command=undo)
    line_button       = tk.Button(root, text="Line", command=line)
    circle_button     = tk.Button(root, text="Circle", command=circle)
    background_button = tk.Button(root, text="Background", command=background)

    line_button.grid(row=0, column=0)
    color_button.grid(row=0, column=1)
    undo_button.grid(row=0, column=2)
    circle_button.grid(row=0, column=3)
    background_button.grid(row=0, column=4)

def circle():
    global line_creator, coords, circle_creator

    canvas.config(cursor="circle")

    if circle_creator:
        circle_creator = False
        coords = []
    else:
        circle_creator = True
        line_creator   = False

def line():
    global line_creator, coords, circle_creator

    canvas.config(cursor="dot")

    if line_creator:
        line_creator = False
        coords = []
    else:
        line_creator   = True
        circle_creator = False

def clicked(event):
    global line_creator, coords, lines, color, circle_creator, circles, moves, slider
    
    if (line_creator or circle_creator) and slider != None:
        canvas.delete(slider)
        slider = None
    if line_creator and len(coords) == 0:
        coords.append(event.x)
        coords.append(event.y)
    elif line_creator and len(coords) != 0:
        if color != "":
            line = canvas.create_line(coords, event.x, event.y, fill=color)
        else:
            line = canvas.create_line(coords, event.x, event.y)
        moves.append(line)
        coords = []
        lines  = []

    if circle_creator and len(coords) == 0:
        coords.append(event.x)
        coords.append(event.y)
    elif circle_creator and len(coords) != 0:
        if color != "":
            circle = canvas.create_oval(coords, event.x, event.y, fill=color)
        else:
            circle = canvas.create_oval(coords, event.x, event.y)
        moves.append(circle)
        coords  = []
        circles = []

def motion(event):
    global line_creator, coords, lines, canvas, color, circle_creator, circles, size_slider
    
    if line_creator:
        if len(coords) != 0:
            try:
                for line in lines:
                    canvas.delete(line)
                    lines.remove(line)
            except IndexError:
                pass

            if color != "":
                line = canvas.create_line(coords, event.x, event.y, fill=color)
            else:
                line = canvas.create_line(coords, event.x, event.y)
            lines.append(line)
    elif circle_creator:
        if len(coords) != 0:
            try:
                for circle in circles:
                    canvas.delete(circle)
                    circles.remove(circle)
            except IndexError:
                pass

            if color != "":
                circle = canvas.create_oval(coords, event.x, event.y, fill=color)
            else:
                circle = canvas.create_oval(coords, event.x, event.y)
            circles.append(circle)
            
def background():
    global bg, canvas, erased
    color = colorchooser.askcolor(title="Choose Background")
    bg = color[1]
    canvas.config(bg=bg)

    for mark in erased:
        new_line = canvas.itemconfig(mark, fill=bg)

def undo():
    global moves
    try:
        canvas.delete(moves[-1])
        moves.remove(moves[-1])
    except IndexError:
        pass

class Draw(object):
    global bg, color, erased
    pen_size = 5.0
    default_color = "black"

    def __init__(self):
        global root, canvas
        self.root = root
        self.pen_button = tk.Button(self.root, text="pen", command=self.pen)
        self.eraser_button = tk.Button(self.root, text="eraser", command=self.erase)
        self.save_button = tk.Button(self.root, text="save", command=self.save)
        
        self.size_slider = size_slider
        self.canvas = canvas

        self.pen_button.grid(row=0, column=5)
        self.eraser_button.grid(row=0, column=6)
        self.save_button.grid(row=0, column=7)
        self.size_slider.grid(row=0, column=8)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.size_slider.get()
        self.color = self.default_color
        self.eraser_on = False
        self.active_button = self.pen_button
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def pen(self):
        self.activate_button(self.pen_button)
        self.canvas.config(cursor="pencil")

    def erase(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def save(self):
        entry = tk.entry(self.root, bd=5)
        entry.grid()
        self.canvas.postscript(file = file_name + '.eps')

    def activate_button(self, button, eraser_mode=False):
        global line_creator, circle_creator
        line_creator = False
        circle_creator = False
        self.active_button.config(relief='raised')
        button.config(relief='sunken')
        self.active_button = button
        self.eraser_on = eraser_mode

    def paint(self, event):
        global color, moves, circle_creator, line_creator, slider
        
        if slider != None:
            canvas.delete(slider)
            slider = None

        if circle_creator or line_creator:
            return False
        if color != "":
            self.color = color
        else:
            self.color = self.default_color
        self.line_width = self.size_slider.get()
        if self.eraser_on:
            canvas.config(cursor="")
            if bg != "":
                paint_color = bg
            else:
                paint_color = "white"
        else:
            paint_color = self.color

        if self.old_x and self.old_y:
            line = self.canvas.create_line(self.old_x, self.old_y, event.x,
                                           event.y, width=self.line_width,
                                           fill=paint_color, capstyle='round',
                                           smooth='true', splinesteps=36)
            if self.eraser_on:
                erased.append(line)
            moves.append(line)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

def main():
    root.geometry("%dx%d+%d+%d" % (width, height, x_shift, y_shift))
    options()

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar)
    file_menu.add_command(label="Undo", command=undo)

    canvas.grid(row=1, columnspan=9)

    canvas.bind("<Button-1>", clicked)
    canvas.bind("<Motion>", motion)

    Draw()

    root.mainloop()

if __name__ == '__main__':
    main()
