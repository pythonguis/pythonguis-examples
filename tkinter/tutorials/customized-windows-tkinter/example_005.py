from tkinter import Tk

# Create the app's main window
root = Tk()
root.title("0.6 Transparency Window")
root.geometry("400x300+300+120")

# Set the -alpha value to 0.6
root.attributes("-alpha", 0.6)

# Run the app's main loop
root.mainloop()
