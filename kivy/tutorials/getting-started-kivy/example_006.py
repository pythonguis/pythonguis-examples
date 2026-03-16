# Getting Started With Kivy for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-kivy/

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

Builder.load_file("labels.kv")
Builder.load_file("buttons.kv")


class CustomLabel(Label):
    pass


class CustomButton(Button):
    pass


class MainApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")
        root.add_widget(CustomLabel())
        root.add_widget(CustomButton())
        return root


MainApp().run()
