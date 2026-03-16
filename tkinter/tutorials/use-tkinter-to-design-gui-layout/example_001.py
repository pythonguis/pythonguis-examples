# Use Tkinter to Design GUI Layouts
# https://www.pythonguis.com/tutorials/use-tkinter-to-design-gui-layout/

import tkinter as tk

root = tk.Tk()
root.title("Frame Demo")
root.config(bg="skyblue")

# Create Frame widget
frame = tk.Frame(root, width=200, height=200)
frame.pack(padx=10, pady=10)

root.mainloop()
