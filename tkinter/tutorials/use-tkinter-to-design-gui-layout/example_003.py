# Use Tkinter to Design GUI Layouts
# https://www.pythonguis.com/tutorials/use-tkinter-to-design-gui-layout/

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Image Editor")

image = tk.PhotoImage(file="forest.png")

# Tools frame
tools_frame = tk.Frame(root, width=200, height=400, bg="skyblue")
tools_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)
tk.Label(
    tools_frame,
    text="Original Image",
    bg="skyblue",
).pack(padx=5, pady=5)
thumbnail_image = image.subsample(5, 5)
tk.Label(tools_frame, image=thumbnail_image).pack(padx=5, pady=5)

# Tools and Filters tabs
notebook = ttk.Notebook(tools_frame)
notebook.pack(expand=True, fill="both")

tools_tab = tk.Frame(notebook, bg="lightblue")
tools_var = tk.StringVar(value="None")
for tool in ["Resizing", "Rotating"]:
    tk.Radiobutton(
        tools_tab,
        text=tool,
        variable=tools_var,
        value=tool,
        bg="lightblue",
    ).pack(anchor="w", padx=20, pady=5)

filters_tab = tk.Frame(notebook, bg="lightgreen")
filters_var = tk.StringVar(value="None")
for filter in ["Blurring", "Sharpening"]:
    tk.Radiobutton(
        filters_tab,
        text=filter,
        variable=filters_var,
        value=filter,
        bg="lightgreen",
    ).pack(anchor="w", padx=20, pady=5)

notebook.add(tools_tab, text="Tools")
notebook.add(filters_tab, text="Filters")

# Image frame
image_frame = tk.Frame(root, width=400, height=400, bg="grey")
image_frame.pack(padx=5, pady=5, side=tk.RIGHT)
display_image = image.subsample(2, 2)
tk.Label(
    image_frame,
    text="Edited Image",
    bg="grey",
    fg="white",
).pack(padx=5, pady=5)
tk.Label(image_frame, image=display_image).pack(padx=5, pady=5)

root.mainloop()
