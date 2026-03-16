# Create Radiobuttons and Checkbuttons in Tkinter
# https://www.pythonguis.com/tutorials/tkinter-radiobutton-and-checkbutton/

import tkinter as tk

root = tk.Tk()
root.title("Checkbutton")
root.geometry("200x100")


def select_items():
    label.config(text=f"Selected: {bool(variable.get())}")


variable = tk.IntVar()
item = tk.Checkbutton(
    root,
    text="Tuna fish",
    command=select_items,
    variable=variable,
)
item.pack(anchor="w", padx=10, pady=10)

label = tk.Label(root, text="Selected: False")
label.pack(
    anchor="w",
    padx=10,
    pady=10,
)

root.mainloop()
