# Getting Started With Kivy for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-kivy/

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget


class CanvasApp(App):
    def build(self):
        root = Widget()
        size = 200
        width, height = Window.size
        pos_x = 1 / 2 * (width - size)
        pos_y = 1 / 2 * (height - size)
        with root.canvas:
            Rectangle(size=[size, size], pos=[pos_x, pos_y])
        return root


CanvasApp().run()
