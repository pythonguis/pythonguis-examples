# Customizing Your Tkinter App's Windows
# https://www.pythonguis.com/tutorials/customized-windows-tkinter/

from tkinter import Tk

# Create the app's main window
root = Tk()
root.title("Window With a Title Bar")
root.geometry("400x300+300+120")

# Run the app's main loop
root.mainloop()
