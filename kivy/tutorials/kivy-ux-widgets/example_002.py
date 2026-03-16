# Basic Kivy Widgets
# https://www.pythonguis.com/tutorials/kivy-ux-widgets/

from pathlib import Path

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

Window.clearcolor = (0, 0.31, 0.31, 1.0)


class ApplicationFormApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=[20, 30])

        logo_path = Path(kivy.__file__).parent / "data" / "logo" / "kivy-icon-512.png"

        layout.add_widget(Image(source=str(logo_path)))

        return layout


ApplicationFormApp().run()
