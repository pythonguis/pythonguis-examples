from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


class WidgetNameApp(App):
    title = "WidgetName Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (360, 640)

        root = BoxLayout()

        return root


WidgetNameApp().run()
