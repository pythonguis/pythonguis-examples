# Create Radiobuttons and Checkbuttons in Tkinter
# https://www.pythonguis.com/tutorials/tkinter-radiobutton-and-checkbutton/

import tkinter as tk
from tkinter import messagebox, ttk


class FoodOrderingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Order Form")
        self.foods_list = ["Burger", "Pizza", "Fries", "Nuggets"]
        self.payment_methods = ["Cash", "Card", "Mobile App"]
        self.setup_header()
        self.setup_foods()
        self.setup_payment()

    def setup_header(self):
        self.image = tk.PhotoImage(file="food.png").subsample(3, 4)
        tk.Label(self, image=self.image).pack()
        tk.Label(
            self,
            text="Order Your Food!",
            font=("Helvetica", 20),
            bd=10,
        ).pack()
        line = ttk.Separator(self, orient=tk.HORIZONTAL)
        line.pack(fill="x")
        order_label = tk.Label(self, text="What would you like to order?")
        order_label.pack(anchor="w", padx=10, pady=5)

    def setup_foods(self):
        for food_item in self.foods_list:
            var = tk.IntVar()
            self.__dict__[food_item] = tk.Checkbutton(
                self, text=food_item, variable=var
            )
            self.__dict__[food_item].var = var
            self.__dict__[food_item].pack(anchor="w", padx=10, pady=5)

    def setup_payment(self):
        payment_label = tk.Label(
            self,
            text="How would you like to pay?",
        )
        payment_label.pack(anchor="w", padx=10, pady=5)

        self.var = tk.IntVar()
        self.var.set(0)

        for value, method in enumerate(self.payment_methods):
            tk.Radiobutton(
                self,
                text=method,
                variable=self.var,
                value=value,
            ).pack(anchor="w", padx=10, pady=5)

        next_button = tk.Button(
            self,
            text="Check out!",
            command=self.print_results,
            font=("Helvetica", 14),
        )
        next_button.pack(padx=10, pady=5)

    def print_results(self):
        msg = ""
        for food_name in self.foods_list:
            food_button = getattr(self, food_name)
            if food_button.var.get() == 1:
                msg += f"Item selected: {food_button['text']}\n"

        index = self.var.get()
        msg += f"Payment method: {self.payment_methods[index]}"
        messagebox.showinfo("Order Summary", msg)


if __name__ == "__main__":
    app = FoodOrderingApp()
    app.mainloop()
