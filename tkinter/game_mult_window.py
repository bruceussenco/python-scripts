import tkinter as tk
import math

class Screen:
    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas


def new_screen(x=0, y=0):
    window = tk.Toplevel()
    window.geometry(f"+{x}+{y}")
    window.overrideredirect(True) # remove top border

    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
    canvas.pack()

    screens.append(Screen(window, canvas))

def line_all(a, b):
    for screen in screens:
        x = screen.window.winfo_x()
        y = screen.window.winfo_y()

        screen.canvas.create_line((a[0] - x, a[1] - y), (b[0] - x, b[1] - y), width=2, fill="red")
        
    
WIDTH = 320
HEIGHT = 200

root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Game")

tk.Button(root, text="Quit", command=root.destroy).pack() 
tk.Button(root, text="Add Line", command=lambda: line_all((100, 100), (1700, 700))).pack()

screens = []

new_screen(320, 200); new_screen(640, 200); new_screen(960, 200)
new_screen(320, 400); new_screen(640, 400); new_screen(960, 400)
new_screen(320, 600); new_screen(640, 600); new_screen(960, 600)

def game_loop():
    global current_time
    for screen in screens:
        newx = math.floor(screen.window.winfo_x() + 5*math.cos(current_time/1000))
        newy = math.floor(screen.window.winfo_y() + 5*math.sin(current_time/1000))
        
        screen.window.geometry(f"+{newx}+{newy}")

    current_time += 100
    root.after(100, game_loop)

current_time = 0
root.after(100, game_loop)

root.mainloop()
