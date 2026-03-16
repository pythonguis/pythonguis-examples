# Customizing Your Tkinter App's Windows
# https://www.pythonguis.com/tutorials/customized-windows-tkinter/

from tkinter import Tk

# Create the app's main window
root = Tk()
root.geometry("400x300+300+120")

# Removes the window's title bar
root.overrideredirect(True)

# Run the app's main loop
root.mainloop()
