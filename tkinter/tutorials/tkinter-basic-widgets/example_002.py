# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk

root = tk.Tk()
root.title("Tkinter Label")
root.geometry("200x80")

label = tk.Label(root, text="Hello!", font=("Helvetica", 30))
label.pack(expand=True)

root.mainloop()
