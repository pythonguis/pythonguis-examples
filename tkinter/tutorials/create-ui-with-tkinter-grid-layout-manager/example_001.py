# Using the Grid Geometry Manager in Tkinter
# https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/

import tkinter as tk

root = tk.Tk()
root.title("The Grid Geometry Manager")

for row in range(3):
    for col in range(3):
        tk.Button(
            root,
            text=f"Cell ({row}, {col})",
            width=10,
            height=5,
        ).grid(row=row, column=col)

tk.Button(root, text="Span 2 columns", height=5).grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="ew",
)
tk.Button(root, text="Span 2 rows", width=10, height=10).grid(
    row=4,
    column=0,
    rowspan=2,
    sticky="ns",
)

root.mainloop()
