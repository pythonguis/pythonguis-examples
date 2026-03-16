import tkinter as tk

root = tk.Tk()

# Setting some window properties
root.title("Tk Example")
root.configure(background="yellow")
root.minsize(200, 200)
root.maxsize(500, 500)
root.geometry("300x300+50+50")

root.mainloop()
