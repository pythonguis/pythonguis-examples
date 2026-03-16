# Create Buttons in Tkinter
# https://www.pythonguis.com/tutorials/create-buttons-in-tkinter/

import tkinter as tk

root = tk.Tk()  # Create the main window

# Create a TV remote UI
turn_on = tk.Button(root, text="ON")
turn_on.pack()

turn_off = tk.Button(root, text="OFF", command=root.destroy)
turn_off.pack()

volume = tk.Label(root, text="VOLUME")
volume.pack()

vol_up = tk.Button(root, text="+")
vol_up.pack()

vol_down = tk.Button(root, text="-")
vol_down.pack()

root.mainloop()
