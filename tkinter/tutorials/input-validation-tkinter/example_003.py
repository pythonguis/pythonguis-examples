# Input Validation in Tkinter GUI Apps
# https://www.pythonguis.com/tutorials/input-validation-tkinter/

from tkinter import Tk, ttk

# Create the app's main window
root = Tk()
root.title("Widget-Level Validation")
root.geometry("490x120")


# Create a validation function
def validate_age():
    age = age_entry.get()
    if age:
        if age.isdigit() and int(age) in range(1, 151):
            label.config(
                text=f"Valid age: {age}",
                foreground="green",
            )
            return True
        else:
            label.config(
                text="Age must be a number between 1 and 150",
                foreground="red",
            )
            return False
    else:
        label.config(
            text="Entry is empty",
            foreground="red",
        )
        return False


# Add widgets
name_label = ttk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(root, width=35)
name_entry.grid(row=0, column=1, padx=5, pady=5)
age_label = ttk.Label(root, text="Age:")
age_label.grid(row=1, column=0, padx=5, pady=5)
age_entry = ttk.Entry(
    root,
    width=35,
    validatecommand=validate_age,
    validate="focusout",
)
age_entry.grid(row=1, column=1, padx=5, pady=5)
label = ttk.Label(root, text="Display")
label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Run the app's main loop
root.mainloop()
