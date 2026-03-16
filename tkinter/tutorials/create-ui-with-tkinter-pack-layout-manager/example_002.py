import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Sign in")
root.resizable(False, False)

tk.Label(
    root,
    text="Sign in to Tkinter",
    font=("Font", 30),
).pack(ipady=5, fill="x")

image = tk.PhotoImage(file="profile.png").subsample(5, 5)
tk.Label(
    root,
    image=image,
    relief=tk.RAISED,
).pack(pady=5)


def check_input():
    secret_username = "username"
    secret_password = "password"
    username = username_entry.get()
    password = password_entry.get()
    if username == secret_username and password == secret_password:
        messagebox.showinfo("Info", "Used logged in!")
    else:
        messagebox.showerror("Error", "Invalid username or password")


# Username and password
tk.Label(root, text="Your username").pack(anchor="w", padx=30)
username_entry = tk.Entry(root)
username_entry.pack(padx=30, fill="x")
tk.Label(root, text="Password").pack(anchor="w", padx=30)
password_entry = tk.Entry(root)
password_entry.pack(padx=30, fill="x")

# Sign in button
tk.Button(
    root,
    text="Sign in",
    command=check_input,
    width=18,
).pack(pady=10, padx=30, fill="x")

# Remember me and forgot password
tk.Checkbutton(
    root,
    text="Remember me",
    command=lambda: print("The check button works."),
).pack(side="left", padx=30, pady=5)
tk.Label(
    root,
    text="Forgot password?",
    fg="blue",
    cursor="hand2",
).pack(side="right", padx=30, pady=5)

root.mainloop()
