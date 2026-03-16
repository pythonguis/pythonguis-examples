import tkinter as tk

root = tk.Tk()
root.title("The Pack Geometry Manager")
root.geometry("340x100")

tk.Button(root, text="Top Button!").pack()

tk.Label(root, text="Hello, Left!").pack(side="left")
tk.Label(root, text="Hello, Right!").pack(side="right")

tk.Checkbutton(
    root,
    text="An option at the bottom!",
).pack(side=tk.BOTTOM)

root.mainloop()
