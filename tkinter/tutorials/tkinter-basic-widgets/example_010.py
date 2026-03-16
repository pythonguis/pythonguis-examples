# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk

root = tk.Tk()
root.title("Tkinter Scale")
root.geometry("200x80")


def value_changed(event):
    label.config(text=event.widget.get())


scale = tk.Scale(root, from_=0, to=10, orient="horizontal")
scale.bind("<Motion>", value_changed)
scale.pack(padx=5, pady=5, fill="x")

# A helper label to show the selected value
label = tk.Label(root, text="0")
label.pack(padx=5, pady=5, fill="x")


root.mainloop()
