# Using the Place Geometry Manager in Tkinter
# https://www.pythonguis.com/tutorials/create-ui-with-tkinter-place-layout-manager/

import tkinter as tk

root = tk.Tk()
root.title("Place layout Example")
root.geometry("300x300+50+100")


def display_selection(event):
    selection = cities_listbox.curselection()
    print(cities_listbox.get(selection))


# Label to display the question
tk.Label(
    root,
    text="Which of the following cities would you like to travel to?",
    wraplength=200,
).place(x=50, y=20)

# Listbox to display the cities
cities_listbox = tk.Listbox(root, selectmode=tk.BROWSE, width=24)
cities_listbox.place(x=40, y=65)
cities = ["Beijing", "Singapore", "Tokyo", "Dubai", "New York"]
for city in cities:
    cities_listbox.insert(tk.END, city)

# Bind the listbox's selection
cities_listbox.bind("<<ListboxSelect>>", display_selection)

# Button to close the app
end_button = tk.Button(root, text="End", command=quit)
end_button.place(x=125, y=250)

root.mainloop()
