# Create Buttons in Tkinter
# https://www.pythonguis.com/tutorials/create-buttons-in-tkinter/

import tkinter as tk

root = tk.Tk()
image = tk.PhotoImage(file="rain.gif")


def turn_tv_on():
    window = tk.Toplevel(root)
    window.title("TV")
    original_image = tk.Label(window, image=image)
    original_image.pack()


def volume_up():
    print("Volume Increase +1")


def volume_down():
    print("Volume Decrease -1")


turn_on = tk.Button(root, text="ON", command=turn_tv_on)
turn_on.pack()

turn_off = tk.Button(root, text="OFF", command=root.destroy)
turn_off.pack()

volume = tk.Label(root, text="VOLUME")
volume.pack()

vol_up = tk.Button(root, text="+", command=volume_up)
vol_up.pack()

vol_down = tk.Button(root, text="-", command=volume_down)
vol_down.pack()

root.mainloop()
