import tkinter as tk

root = tk.Tk()  # Create the main window


def volume_up():
    print("Volume Increased +1")


# Create the volume up button
vol_up = tk.Button(root, text="+", command=volume_up)
vol_up.pack()

root.mainloop()
