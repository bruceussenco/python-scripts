import tkinter as tk

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
        print(x, y)

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


root.mainloop()
