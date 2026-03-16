# Input Validation in Tkinter GUI Apps
# https://www.pythonguis.com/tutorials/input-validation-tkinter/

from tkinter import Tk, ttk

# Create the app's main window
root = Tk()
root.title("Form-Level Input Validation")
root.geometry("490x100")


# Create a validation function
def validate_numbers():
    input_data = entry.get()
    if input_data:
        try:
            float(input_data)
            label.config(
                text=f"Valid numeric value: {input_data}",
                foreground="green",
            )
        except ValueError:
            label.config(
                text=f'Numeric value expected, got "{input_data}"',
                foreground="red",
            )
    else:
        label.config(
            text="Entry is empty",
            foreground="red",
        )


# Add widgets
entry = ttk.Entry(root, width=35)
entry.grid(row=0, column=0, padx=5, pady=5)
button = ttk.Button(root, text="Validate", command=validate_numbers)
button.grid(row=0, column=1, padx=5, pady=5)
label = ttk.Label(root, text="Display")
label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Run the app's main loop
root.mainloop()
