import tkinter as tk

def new_window(x=0, y=0):
    window = tk.Toplevel()
    window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    windows.append(window)

def edit_windows():
    for window in windows:
        tk.Label(window, text="test").pack()
    
WIDTH = 320
HEIGHT = 200
POS_X = 20
POS_Y = 20

root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")
root.title("Multiple Windows")
#root.overrideredirect(1) # remove top border

button = tk.Button(root, text="Add", command=lambda: new_window(1400, 700))
button.pack()
tk.Button(root, text="Edit", command=edit_windows).pack()
tk.Button(root, text="Quit", command=root.destroy).pack() 

windows = []

root.mainloop()
