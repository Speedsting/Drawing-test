#!/usr/bin/python
#animation_runner.py
__author__ = "Elijah"
__version__ = 3.6

import tkinter as tk
import painter
from tkinter import colorchooser
import platform

system = ""
if platform.system() == "Darwin":
    system = "mac"

height  = 500
width   = 2000
x_shift = 0
y_shift = 20

slider = None
master = None

bg = "white"

circle_creator = False
line_creator   = False
square_creator = False
sizer          = False
fill_mode      = False

coords     = []
circles    = []
erased     = []
lines      = []
moves      = []
squares    = []
undo_list  = []

root = tk.Tk()
root.title("Animation")
root.geometry("%dx%d+%d+%d" % (width, height, x_shift, y_shift))

def set_color():
    """Sets the current default color"""

    global color
    current_color = colorchooser.askcolor(title="Choose color")
    color = current_color[1]
    pen_draw.color = color

# def create_circle_slider(event=1):
#     """Creates a size circle that represents the brush size
# 
#     :param event: the current size of the brush
#     :return: None"""
# 
#     global pen_size_slider, width, height, slider
#     
#     #gets the value of the pen size
#     amt = float(pen_size_slider.get())
#     amt //= 2
#     
#     height_pos = (height - 60) // 2
#     width_pos  = (width - 35) // 2
#     
#     #makes a circle the same size as the pen
#     canvas.delete(slider)
#     current_coords = [width_pos - amt, height_pos - amt, width_pos + amt, height_pos + amt]
#     slider = canvas.create_oval(current_coords, fill="white", outline="black")
#     
#     pen_draw.slider = slider

canvas = tk.Canvas(root, width=width - 35, height=height - 60, bg=bg)
canvas.grid(row=0, column=3, rowspan=12)

color_btn = tk.Button(root, text="Color", command=set_color)
pen_size_slider = tk.Scale(root, from_=1, to=30, orient="horizontal")

color    = ""
pen_draw = ""

def create_buttons():
    """Creates the buttons for the main screen"""
    undo_btn       = tk.Button(root, text="Undo", command=undo)
    redo_btn       = tk.Button(root, text="Redo", command=redo)
    line_btn       = tk.Button(root, text="Line", command=set_line_mode)
    circle_btn     = tk.Button(root, text="Circle", command=set_circle_mode)
    background_btn = tk.Button(root, text="Background", command=set_background)
    size_btn       = tk.Button(root, text="Size", command=set_pen_size)
    square_btn     = tk.Button(root, text="Square", command=set_square_mode)
    fill_btn       = tk.Button(root, text="Fill", command=set_fill_mode)
    clear_btn      = tk.Button(root, text="Clear", command=check)

    line_btn.grid(row=0, column=0)
    circle_btn.grid(row=1, column=0)
    square_btn.grid(row=2, column=0)
    color_btn.grid(row=3, column=0)
    fill_btn.grid(row=4, column=0)
    background_btn.grid(row=5, column=0)
    size_btn.grid(row=6, column=0)
    undo_btn.grid(row=7, column=0)
    redo_btn.grid(row=8, column=0)
    clear_btn.grid(row=9, column=0)

def set_circle_mode():
    """Turns on circle mode if the circle button is clicked"""

    global line_creator, coords, circle_creator, square_creator, fill_mode
    canvas.config(cursor="circle")
    
    #checks if circle mode is already active
    if circle_creator:
        circle_creator = False
        coords = []
        canvas.config(cursor="")
    else:
        circle_creator = True
        line_creator   = False
        square_creator = False
        fill_mode      = False
        
    pen_draw.circle_creator = circle_creator
    pen_draw.line_creator   = line_creator
    pen_draw.square_creator = square_creator
    pen_draw.fill_mode      = fill_mode
    pen_draw.draw_mode      = False

def set_line_mode():
    """Turns on line mode if the line button is clicked"""

    global line_creator, coords, circle_creator, square_creator, fill_mode
    canvas.config(cursor="cross")
    
    if line_creator:
        line_creator = False
        coords = []
        canvas.config(cursor="")
    else:
        line_creator   = True
        fill_mode      = False
        circle_creator = False
        square_creator = False
        
    pen_draw.circle_creator = circle_creator
    pen_draw.line_creator   = line_creator
    pen_draw.square_creator = square_creator
    pen_draw.fill_mode      = fill_mode
    pen_draw.draw_mode      = False
    
def set_square_mode():
    """Turns on square mode if the square button is clicked"""
    
    global line_creator, coords, circle_creator, square_creator, fill_mode
    canvas.config(cursor="dotbox")
    
    if square_creator:
        square_creator = False
        coords = []
        canvas.config(cursor="")
    else:
        square_creator = True
        line_creator   = False
        circle_creator = False
        fill_mode      = False
    
    pen_draw.circle_creator = circle_creator
    pen_draw.line_creator   = line_creator
    pen_draw.square_creator = square_creator
    pen_draw.fill_mode      = fill_mode
    pen_draw.draw_mode      = False

def set_fill_mode():
    """Turns on fill mode"""
    
    global circle_creator, square_creator, line_creator, fill_mode, coords
    
    if fill_mode:
        fill_mode = False
        coords = []
        canvas.config(cursor="")
    else:
        fill_mode      = True
        square_creator = False
        line_creator   = False
        circle_creator = False
    
    pen_draw.circle_creator = circle_creator
    pen_draw.line_creator   = line_creator
    pen_draw.square_creator = square_creator
    pen_draw.fill_mode      = fill_mode
    pen_draw.draw_mode      = False

def set_pen_size():
    """Creates the slider for the brush size"""
    
    global pen_size_slider, sizer, slider, pen_draw
    
    #removes the slider if its already on the canvas
    sizer = not sizer
    
    if not sizer:
        pen_size_slider.grid_forget()
        canvas.delete(slider)
        slider = None
        
    else:
        pen_size_slider.grid(row=5, column=1, rowspan=1, columnspan=1)
    
    pen_draw.pen_size_slider = pen_size_slider

def clicked(event):
    """Starts a circle or line at where the click occured

    :param event: the place that was clicked
    :return: False is draw mode is on"""

    global line_creator, coords, lines, color, circle_creator, pen_size_slider
    global circles, moves, slider, square_creator, squares, fill_mode
    
    #checks if pen mode is on
    if pen_draw.draw_mode:
        circle_creator = False
        line_creator   = False
        square_creator = False
        return False
    
    #removes the size slider if its on
    if (line_creator or circle_creator or square_creator) and slider != None:
        canvas.delete(slider)
        slider = None
    
    if line_creator and len(coords) == 0:
        coords.append(event.x)
        coords.append(event.y)
    
    #checks to see if there is a color chosen
    elif line_creator and len(coords) != 0:
        size = pen_size_slider.get()
        if color != "":
            line = canvas.create_line(coords, event.x, event.y, fill=color, width=size)
        else:
            line = canvas.create_line(coords, event.x, event.y, width=size)
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
    
    if square_creator and len(coords) == 0:
        coords.append(event.x)
        coords.append(event.y)
    
    elif square_creator and len(coords) != 0:
        if color != "":
            square = canvas.create_rectangle(coords, event.x, event.y, fill=color)
        else:
            square = canvas.create_rectangle(coords, event.x, event.y)
        moves.append(square)
        coords = []
        
        for shape in squares:
            canvas.delete(shape)
        squares = []
    
    elif fill_mode:
        if color != "":
            for i in moves:
                x1, y1, x2, y2 = canvas.coords(i)
                if x1 < event.x < x2 and y1 < event.y < y2:
                    canvas.itemconfig(i, fill=color)
            

def draw_shape(event):
    """Draws either the circle or line depending on which mode is active

    :param event: the place where the mouse is
    :return: None"""

    global line_creator, coords, lines, canvas, color, circle_creator, circles
    global pen_size_slider, square_creator, squares
    
    #creates a line if line mode is active
    if line_creator:
        if len(coords) != 0:
            try:
                for line in lines:
                    canvas.delete(line)
                    lines.remove(line)
            except IndexError:
                pass
            
            size = pen_size_slider.get()

            if color != "":
                line = canvas.create_line(coords, event.x, event.y,
                                          width=size, fill=color)
            else:
                line = canvas.create_line(coords, event.x, event.y, width=size)
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
    
    #creates a square if square mode is active
    elif square_creator:
        if len(coords) != 0:
            try:
                for square in squares:
                    canvas.delete(square)
                    squares.remove(square)
            except IndexError:
                pass
            
            if color != "":
                square = canvas.create_rectangle(coords, event.x, event.y, fill=color)
            else:
                square = canvas.create_rectangle(coords, event.x, event.y)
            squares.append(square)
            
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
    
    coords_list = []
    #tries to remove the most recent move
    try:
        move = moves[-1]
        num = 10000
        if type(move) is list:
            for i in move:
                canvas.move(i, num, num)
        else:
            canvas.move(move, num, num)
        
        moves.remove(move)
        
        undo_list.append(move)
    except IndexError:
        pass
    
    pen_draw.moves = moves

def redo():
    """Re-does the most recent move that was un-done"""
    global moves, undo_list
    
    #tries to redo the most recent un-done move
    try:
        move = undo_list[-1]
        num = -10000
        
        if type(move) is list:
            for i in move:
                canvas.move(i, num, num)   
        else:
            canvas.move(move, num, num)
            
        undo_list.remove(move)
        moves.append(move)
        
    except IndexError:
        pass
    
    pen_draw.moves = moves

class Fullscreen:
    def __init__(self, canvas, root, height, width, x_shift, y_shift):
        """Enables fullscreen if the user toggles fullscreen
        
        :param canvas: the drawing canvas
        :param root: the tkinter window
        :param height: the height of the window
        :param width: the width of the window
        :param x_shift: the amount the window is shifted horizontally
        :param y_shift: the amount the window is shifted vertically
        :return: None"""
        
        self.canvas  = canvas
        self.root    = root
        self.height  = height
        self.width   = width
        self.x_shift = x_shift
        self.y_shift = y_shift
        
        self.state = False

    def toggle_fullscreen(self, event=None):
        """Toggles fullscreen mode
        
        :param event: the key that was pressed
        :return: None"""
        
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)
        
        screen_height = root.winfo_screenheight()
        screen_width  = root.winfo_screenwidth() - 35
        
        #sets the window to its original size if it exits fullscreen
        if not self.state:
            self.canvas.config(height = self.height - 60, width = self.width - 35)
            self.root.geometry("%dx%d+%d+%d" % (self.width, self.height,
                                                self.x_shift, self.y_shift))
        else:
            self.canvas.config(height=screen_height, width=screen_width)

    def end_fullscreen(self, event=None):
        """Ends the fullscreen mode
        
        :param event: the key that was pressed
        :return: None"""
        
        self.state = False
        self.root.attributes("-fullscreen", False)
        
        #sets the window back to its original size
        self.canvas.config(height = self.height - 60, width = self.width - 35)
        self.root.geometry("%dx%d+%d+%d" % (self.width, self.height,
                                            self.x_shift, self.y_shift))

def check():
    """Checks with the user to see if they really want to clear the canvas"""
    
    global master
    master = tk.Tk()
    master.title("")
    label = tk.Label(master, text="Are you sure you wish to clear the board?")
    yes_btn = tk.Button(master, text="Yes", command=clear)
    no_btn  = tk.Button(master, text="No", command=stop)
    
    label.pack()
    yes_btn.pack()
    no_btn.pack()

def clear():
    """Clears the canvas"""
    
    global canvas
    stop()
    canvas.delete("all")
    canvas.config(bg="white")
    

def stop():
    """Deletes the extra window"""
    
    global master
    master.destroy()
    master = None
    
def main():
    """Starts the whole program and listens for mouse clicks"""
    global pen_draw, height, width, x_shift, y_shift
    
    create_buttons()
    window   = Fullscreen(canvas, root, height, width, x_shift, y_shift)
    pen_draw = painter.Draw_tools(bg, canvas, color, circle_creator, erased,
                                  fill_mode, height, line_creator, moves, root,
                                  sizer, square_creator, pen_size_slider, width,
                                  x_shift, y_shift)
    
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    edit_menu = tk.Menu(menubar, tearoff=0)
    view_menu = tk.Menu(menubar, tearoff=0)
    
    edit_menu.add_command(label="Undo", command=undo)
    edit_menu.add_command(label="Redo", command=redo)
    file_menu.add_command(label="Save", command=pen_draw.save)
    view_menu.add_command(label="Fullscreen", command=window.toggle_fullscreen)
    
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    menubar.add_cascade(label="View", menu=view_menu)
    root.config(menu=menubar)
    
    
    canvas.bind("<Button-1>", clicked)
    canvas.bind("<Motion>", draw_shape)
    
    if system == "mac":
        root.bind("<Command-z>", lambda x: undo())
        root.bind("<Command-y>", lambda x: redo())
        root.bind("<Command-Shift-f>", window.toggle_fullscreen)
    else:
        root.bind("<Control-z>", lambda x: undo())
        root.bind("<Control-y>", lambda x: redo())
        root.bind("<Control-Shift-f>", window.toggle_fullscreen)
        
    root.bind("<Escape>", window.end_fullscreen)
    
    root.mainloop()

if __name__ == '__main__':
    main()
