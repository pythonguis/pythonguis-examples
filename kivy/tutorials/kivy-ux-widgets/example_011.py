# Basic Kivy Widgets
# https://www.pythonguis.com/tutorials/kivy-ux-widgets/

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

Window.clearcolor = (0, 0.31, 0.31, 1.0)


class MainApp(App):
    def build(self):
        vertical_slider = Slider(
            min=0,
            max=100,
            value=50,
            step=10,
            orientation="vertical",
        )
        horizontal_slider = Slider(
            min=0,
            max=100,
            value=50,
        )

        layout = BoxLayout()
        layout.add_widget(vertical_slider)
        layout.add_widget(horizontal_slider)

        return layout


MainApp().run()
