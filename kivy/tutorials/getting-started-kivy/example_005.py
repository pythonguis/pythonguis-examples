# Getting Started With Kivy for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-kivy/

from kivy.app import App
from kivy.uix.label import Label


class CustomLabel(Label):
    pass


class MainApp(App):
    def build(self):
        root = CustomLabel()
        return root


MainApp().run()
