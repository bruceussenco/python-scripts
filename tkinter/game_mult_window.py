import tkinter as tk
import math

class Screen:
    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def new_screen(x=0, y=0):
    window = tk.Toplevel()
    window.geometry(f"+{x}+{y}")
    window.overrideredirect(True) # remove top border

    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
    canvas.pack()

    screens.append(Screen(window, canvas))

def add_line(a, b): lines.append(Line(a, b))
    
WIDTH = 320
HEIGHT = 200

root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Game")

# move screen
x_offset = 0
y_offset = 0
def add_offset(x, y):
    global x_offset, y_offset
    x_offset += x
    y_offset += y
tk.Button(root, text="^", command=lambda:add_offset(0,-10)).grid(column=1, row=0)
tk.Button(root, text="<", command=lambda:add_offset(-10,0)).grid(column=0, row=1)
tk.Button(root, text="v", command=lambda:add_offset( 0,10)).grid(column=1, row=1)
tk.Button(root, text=">", command=lambda:add_offset(10, 0)).grid(column=2, row=1)

screens = []
lines   = []

new_screen(320, 200); new_screen(640, 200)
new_screen(320, 400); new_screen(640, 400)

def game_init():
    add_line((100, 100), (1700, 700))
    add_line((800, 300), ( 100, 900))

def game_loop():
    global current_time, x_offset, y_offset

    # clear canvas
    for screen in screens: screen.canvas.delete("all")

    # move screens / rendering
    for screen in screens:
        x = screen.window.winfo_x() + x_offset
        y = screen.window.winfo_y() + y_offset
        
        screen.window.geometry(f"+{x}+{y}")

        # draw lines
        for l in lines:
            screen.canvas.create_line(
                (l.a[0] - x, l.a[1] - y),
                (l.b[0] - x, l.b[1] - y),
                width=2, fill="red"
            )
    x_offset = 0
    y_offset = 0

    current_time += 100
    root.after(100, game_loop)

# game
current_time = 0
game_init()
root.after(100, game_loop)

root.mainloop()

