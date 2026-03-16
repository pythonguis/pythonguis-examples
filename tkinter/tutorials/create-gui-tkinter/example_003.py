import tkinter as tk

root = tk.Tk()
root.title("Tk Example")
root.minsize(200, 200)
root.geometry("300x300+50+50")

# Create two labels
tk.Label(root, text="Nothing will work unless you do.").pack()
tk.Label(root, text="- Maya Angelou").pack()

root.mainloop()
