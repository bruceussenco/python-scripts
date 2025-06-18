import tkinter as tk


# Create the main window
root = tk.Tk()
root.title("Tkinter Example")
root.geometry("320x200")

# Add a label
label = tk.Label(root, text="Click the button!")
label.grid()

# Add a button
def on_button_click(): label.config(text="Hello, World!")
button = tk.Button(root, text="Click Me", command=on_button_click)
button.grid(column=0, row=1)

tk.Button(root, text="Quit", command=root.destroy).grid(column=0, row=2)

# Run the application
root.mainloop()
