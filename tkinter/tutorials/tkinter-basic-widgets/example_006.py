# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tkinter Combobox")
root.geometry("200x80")


def selection_changed(event):
    label.config(text=f"{event.widget.get()} selected!")


combobox = ttk.Combobox(root, values=["One", "Two", "Three"])
combobox.set("One")
combobox.bind("<<ComboboxSelected>>", selection_changed)
combobox.pack(padx=5, pady=5, fill="x")

# A helper label to show the selected value
label = tk.Label(root, text="One selected!")
label.pack(padx=5, pady=5, fill="x")


root.mainloop()
