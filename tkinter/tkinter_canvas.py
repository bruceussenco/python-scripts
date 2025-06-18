import tkinter as tk

root = tk.Tk()
root.geometry('800x600')
root.title('Canvas Demo')

canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.pack(anchor=tk.CENTER, expand=True)

canvas.create_rectangle((100, 100), (300, 300), fill='green')

points = (
    (50, 150),
    (200, 350),
)
canvas.create_oval(*points, fill='purple')

points = (
    (100, 300),
    (200, 200),
    (300, 300),
)
canvas.create_polygon(*points, fill='blue')

canvas.create_text(
    (300, 50),
    text="Canvas Demo",
    fill="orange",
    font='tkDefaeultFont 24'
)

canvas.create_arc((400,  10), (590, 200), style=tk.PIESLICE, width=2)
canvas.create_arc((400, 160), (590, 350), style=tk.CHORD,    width=2)
canvas.create_arc((400, 300), (590, 490), style=tk.ARC,      width=2)


root.mainloop()