# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk

root = tk.Tk()
root.title("Tkinter Label Image")

photo = tk.PhotoImage(file="otje.png").subsample(2)
label = tk.Label(root, image=photo)
label.pack(expand=True)

root.mainloop()
