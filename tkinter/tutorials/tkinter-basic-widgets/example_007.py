# Tkinter Widgets
# https://www.pythonguis.com/tutorials/tkinter-basic-widgets/

import tkinter as tk

root = tk.Tk()
root.title("Tkinter Listbox")


def selection_changed(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        label.config(text=f"{event.widget.get(index)} selected!")
        event.widget.get(index)


listbox = tk.Listbox(root)
for item in ["One", "Two", "Three"]:
    listbox.insert(tk.END, item)
listbox.bind("<<ListboxSelect>>", selection_changed)
listbox.pack(padx=5, pady=5, fill="both", expand=True)

# A helper label to show the selected value
label = tk.Label(root, text="One selected!")
label.pack(padx=5, pady=5, fill="x")


root.mainloop()
