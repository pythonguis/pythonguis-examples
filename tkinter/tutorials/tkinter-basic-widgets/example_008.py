# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk

root = tk.Tk()
root.title("Tkinter Entry")


def return_pressed(event):
    label.config(text=event.widget.get())


entry = tk.Entry(root)
entry.insert(0, "Enter your text")
entry.bind("<Return>", return_pressed)
entry.pack(padx=5, pady=5, fill="x")

# A helper label to show the selected value
label = tk.Label(root, text="Entry demo!")
label.pack(padx=5, pady=5, fill="x")


root.mainloop()
