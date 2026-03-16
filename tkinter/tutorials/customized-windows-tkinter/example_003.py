from tkinter import Tk

# Create the app's main window
root = Tk()
root.title("Fixed Size Window")
root.geometry("400x300+300+120")

# Disable the window's resizing capability
root.resizable(False, False)

# Run the app's main loop
root.mainloop()
