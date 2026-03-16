# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk

root = tk.Tk()
root.title("Tkinter Button")
root.geometry("200x100")


def on_click():
    label.config(text="Button clicked!")


button = tk.Button(
    root,
    text="Click Me",
    command=on_click,
)
button.pack(padx=5, pady=5)

# A helper label to show the result of the click
label = tk.Label(root, text="Waiting for click...")
label.pack(padx=5, pady=5)

root.mainloop()
