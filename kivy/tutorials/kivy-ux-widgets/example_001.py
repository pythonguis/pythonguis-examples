# Basic Kivy Widgets
# https://www.pythonguis.com/tutorials/kivy-ux-widgets/

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

Window.clearcolor = (0, 0.31, 0.31, 1.0)


class ApplicationFormApp(App):
    def build(self):
        layout = BoxLayout()
        return layout


ApplicationFormApp().run()
