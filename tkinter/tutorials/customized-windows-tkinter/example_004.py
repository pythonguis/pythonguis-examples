# Customizing Your Tkinter App's Windows
# https://www.pythonguis.com/tutorials/customized-windows-tkinter/

from tkinter import Tk

# Create the app's main window
root = Tk()
root.title("Zoomed Window")
root.geometry("400x300+300+120")

# Set the window to a zoomed mode
root.state("zoomed")

# Run the app's main loop
root.mainloop()
