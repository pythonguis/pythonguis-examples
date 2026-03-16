import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Complete Your Profile")
root.resizable(False, False)

# Profile image
image = tk.PhotoImage(file="profile.png").subsample(6, 6)
tk.Label(
    root,
    image=image,
    relief=tk.RAISED,
).grid(row=0, column=0, rowspan=5, padx=10, pady=10)

# Name field
tk.Label(
    root,
    text="Name:",
).grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
name = ttk.Entry(root)
name.grid(row=0, column=2, padx=5, pady=5, ipadx=5)

# Gender field
tk.Label(
    root,
    text="Gender:",
).grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
gender = ttk.Combobox(
    root,
    values=["Male", "Female", "Other"],
    state="readonly",
)
gender.grid(row=1, column=2, padx=5, pady=5)

# Eye color field
tk.Label(
    root,
    text="Eye Color:",
).grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
eye_color = ttk.Combobox(
    root,
    values=["Brown", "Green", "Blue", "Black", "Other"],
    state="readonly",
)
eye_color.grid(row=2, column=2, padx=5, pady=5)

# Height field
tk.Label(
    root,
    text="Height (cm):",
).grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
height = ttk.Entry(root)
height.grid(row=3, column=2, padx=5, pady=5, ipadx=5)

# Weight field
tk.Label(
    root,
    text="Weight (kg):",
).grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)
weight = ttk.Entry(root)
weight.grid(row=4, column=2, padx=5, pady=5, ipadx=5)

# Submit button
submit = ttk.Button(
    root,
    text="Submit",
)
submit.grid(row=5, column=2, padx=5, pady=5, sticky=tk.E)

root.mainloop()
