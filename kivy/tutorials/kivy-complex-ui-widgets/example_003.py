from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class DropDownApp(App):
    title = "DropDown Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (200, 200)

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Create a dropdown with 4 buttons
        dropdown = DropDown()
        for item in ["Kivy", "PyQt6", "PySide6", "Tkinter"]:
            option_btn = Button(text=item, size_hint_y=None, height=50, width=150)
            option_btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(option_btn)

        # Create a main button to show the dropdown
        button = Button(
            text="Library",
            size_hint=(None, None),
            size=(150, 50),
        )
        button.bind(on_release=dropdown.open)
        dropdown.bind(
            on_select=lambda instance, text: setattr(button, "text", text),
        )
        root.add_widget(button)
        return root


DropDownApp().run()
