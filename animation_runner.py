#!/usr/bin/python
#animation_runner.py
__author__ = "Elijah"
__version__ = 3.1

import tkinter as tk
import painter
from tkinter import colorchooser

height  = 500
width   = 900
x_shift = 0
y_shift = 20

slider   = None

bg = "white"

circle_creator = False
line_creator   = False
sizer          = False

coords    = []
circles   = []
erased    = []
lines     = []
moves     = []
undo_list = []

root = tk.Tk()
root.title("Animation")
root.geometry("%dx%d+%d+%d" % (width, height, x_shift, y_shift))

def set_color():
    """Sets the current default color"""

    global color
    current_color = colorchooser.askcolor(title="Choose color")
    color = current_color[1]
    pen_draw.color = color

def create_circle_slider(event=1):
    """Creates a size circle that represents the brush size

    :param event: the current size of the brush
    :return: None"""

    global pen_size_slider, width, height, slider
    
    #gets the value of the pen size
    amt = float(pen_size_slider.get())
    amt //= 2
    
    height_pos = height // 2
    width_pos  = width // 2
    
    #makes a circle the same size as the pen
    canvas.delete(slider)
    current_coords = [width_pos - amt, height_pos - amt, width_pos + amt, height_pos + amt]
    slider = canvas.create_oval(current_coords, fill="white", outline="black")
    
    pen_draw.slider = slider

canvas = tk.Canvas(root, width=width - 35, height=height - 60, bg=bg)
canvas.grid(row=2, column=1, columnspan=10)

color_btn = tk.Button(root, text="Color", command=set_color)
pen_size_slider = tk.Scale(root, from_=1, to=30, orient="horizontal", command=create_circle_slider)

color    = ""
pen_draw = ""

def create_buttons():
    """Creates the buttons for the main screen"""
    undo_btn       = tk.Button(root, text="Undo", command=undo)
    line_btn       = tk.Button(root, text="Line", command=set_line_mode)
    circle_btn     = tk.Button(root, text="Circle", command=set_circle_mode)
    background_btn = tk.Button(root, text="Background", command=set_background)
    size_btn       = tk.Button(root, text="Size", command=set_pen_size)

    line_btn.grid(row=0, column=0)
    color_btn.grid(row=0, column=1)
    undo_btn.grid(row=0, column=2)
    circle_btn.grid(row=0, column=3)
    background_btn.grid(row=0, column=4)
    size_btn.grid(row=0, column=5)

def set_circle_mode():
    """Turns on circle mode if the circle button is clicked"""

    global line_creator, coords, circle_creator
    canvas.config(cursor="circle")
    
    #checks if circle mode is already active
    if circle_creator:
        circle_creator = False
        coords = []
    else:
        circle_creator = True
        line_creator   = False
    pen_draw.circle_creator = circle_creator
    pen_draw.line_creator   = line_creator
    pen_draw.draw_mode      = False

def set_line_mode():
    """Turns on line mode if the line button is clicked"""

    global line_creator, coords, circle_creator
    canvas.config(cursor="dot")
    
    if line_creator:
        line_creator = False
        coords = []
    else:
        line_creator   = True
        circle_creator = False
    
    pen_draw.circle_creator = circle_creator
    pen_draw.line_creator   = line_creator
    pen_draw.draw_mode      = False

def set_pen_size():
    """Creates the slider for the brush size
    
    :return: False if slider is already open"""
    
    global pen_size_slider, sizer, pen_draw, slider
    
    #removes the slider if its already on the canvas
    if sizer:
        sizer = False
        pen_size_slider.grid_forget()
        canvas.delete(slider)
        slider = None
        
        return False
    
    else:
        sizer = True
        create_circle_slider()
    
    pen_draw.sizer  = sizer
    pen_draw.slider = slider
    
    pen_size_slider.grid(row=1, column=5, rowspan=1, columnspan=1)

def clicked(event):
    """Starts a circle or line at where the click occured

    :param event: the place that was clicked
    :return: False is draw mode is on"""

    global line_creator, coords, lines, color, circle_creator, circles, moves, slider
    
    #checks if pen mode is on
    if pen_draw.draw_mode:
        circle_creator = False
        line_creator   = False
        return False
    
    #removes the size slider if its on
    if (line_creator or circle_creator) and slider != None:
        canvas.delete(slider)
        slider = None
    
    if line_creator and len(coords) == 0:
        coords.append(event.x)
        coords.append(event.y)
    
    #checks to see if there is a color chosen
    elif line_creator and len(coords) != 0:
        if color != "":
            line = canvas.create_line(coords, event.x, event.y, fill=color)
        else:
            line = canvas.create_line(coords, event.x, event.y)
        moves.append(line)
        coords = []
        
        for shape in lines:
            canvas.delete(shape)
        lines = []

    if circle_creator and len(coords) == 0:
        coords.append(event.x)
        coords.append(event.y)
    
    #checks to see if there is a color chosen
    elif circle_creator and len(coords) != 0:
        if color != "":
            circle = canvas.create_oval(coords, event.x, event.y, fill=color)
        else:
            circle = canvas.create_oval(coords, event.x, event.y)
        moves.append(circle)
        coords  = []
        
        for shape in circles:
            canvas.delete(shape)
        circles = []

def draw_shape(event):
    """Draws either the circle or line depending on which mode is active

    :param event: the place where the mouse is
    :return: None"""

    global line_creator, coords, lines, canvas, color, circle_creator, circles, pen_size_slider
    
    #creates a line if line mode is active
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
    
    #creates a circle is circle mode is active
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
            
def set_background():
    """Sets the background color based on the user's choice"""

    global bg, canvas, erased
    
    #gets the new background color
    current_color = colorchooser.askcolor(title="Choose Background")
    bg = current_color[1]
    pen_draw.canvas.config(bg=bg)
    
    #changes every erase mark to the color of the background
    for mark in erased:
        new_line = canvas.itemconfig(mark, fill=bg)
    
    pen_draw.bg = bg

def undo():
    """Un-does the most recent move made by the user"""
    global moves, undo_list
    
    #tries to remove the most recent move
    try:
        move = moves[-1]
        canvas.delete(move)
        moves.remove(move)
        
        undo_list.append(move)
    except IndexError:
        pass
    
    pen_draw.moves = moves

def redo():
    """Re-does the most recent move that was un-done by the user"""
    global moves, undo_list
    
    try:
        move = undo_list[-1]
        #DNF
    except IndexError:
        pass

def main():
    """Starts the whole program and listens for mouse clicks"""
    global pen_draw
    
    create_buttons()
    pen_draw = painter.Draw_tools(bg, canvas, color, circle_creator, erased,
                line_creator, moves, root, sizer, pen_size_slider, slider)
    
    canvas.bind("<Button-1>", clicked)
    canvas.bind("<Motion>", draw_shape)
    root.mainloop()

if __name__ == '__main__':
    main()
