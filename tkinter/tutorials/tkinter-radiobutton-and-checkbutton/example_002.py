# Create Radiobuttons and Checkbuttons in Tkinter
# https://www.pythonguis.com/tutorials/tkinter-radiobutton-and-checkbutton/

import tkinter as tk

root = tk.Tk()
root.title("Radiobutton")
root.geometry("180x240")

countries = ["USA", "France", "Germany", "Sweden", "Brazil"]

label = tk.Label(
    root,
    text=f"Selected: {countries[0]}",
)
label.pack(anchor="w", padx=10, pady=10)


def selection():
    label.config(text=f"Selected: {variable.get()}")


variable = tk.StringVar(root, f"{countries[0]}")

for country in countries:
    tk.Radiobutton(
        root,
        text=country,
        variable=variable,
        value=country,
        command=selection,
    ).pack(anchor="w", padx=10, pady=5)

root.mainloop()
