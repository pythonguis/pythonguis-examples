import csv

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView


class EmployeesView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employees_data = self._read_from_csv()

        # Load the employees data into the data attribute
        self.data = [
            {
                "text": f"{employee['name']}",
                "on_release": self._create_callback(employee["name"]),
            }
            for employee in self.employees_data
        ]

        layout_manager = RecycleBoxLayout(
            default_size=(None, dp(56)),
            default_size_hint=(1, None),
            size_hint_y=None,
            orientation="vertical",
        )
        layout_manager.bind(minimum_height=layout_manager.setter("height"))

        self.add_widget(layout_manager)
        self.viewclass = "Button"

    def _create_callback(self, name):
        return lambda: self.on_button_click(name)

    def _read_from_csv(self):
        with open("employees.csv", mode="r") as file:
            return [row for row in csv.DictReader(file)]

    def on_button_click(self, name):
        popup = Popup(
            title=f"{name}'s Profile",
            size_hint=(0.8, 0.5),
            size=(300, 300),
            auto_dismiss=False,
        )
        employees_data = [
            employee for employee in self.employees_data if employee["name"] == name
        ]
        profile = "\n".join(
            [f"{key.capitalize()}: {value}" for key, value in employees_data[0].items()]
        )
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        message = Label(text=profile)
        ok_button = Button(text="OK", size_hint=(None, None))
        ok_button.bind(on_release=popup.dismiss)
        layout.add_widget(message)
        layout.add_widget(ok_button)
        popup.content = layout
        popup.open()


class RecycleViewApp(App):
    title = "RecycleView Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (360, 640)

        return EmployeesView()


RecycleViewApp().run()
