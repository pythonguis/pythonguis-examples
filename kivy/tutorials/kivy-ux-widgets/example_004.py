# Basic Kivy Widgets
# https://www.pythonguis.com/tutorials/kivy-ux-widgets/

from pathlib import Path

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput  # <-- update

YELLOW = (1, 1, 0, 1)

Window.clearcolor = (0, 0.31, 0.31, 1.0)


class ApplicationFormApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=[20, 30])

        logo_path = Path(kivy.__file__).parent / "data" / "logo" / "kivy-icon-512.png"
        title_label = Label(text="Application Form", color=YELLOW, font_size=24)
        fullname_label = Label(text="Full Name", color=YELLOW, font_size=20)
        about_label = Label(text="About Yourself", color=YELLOW, font_size=20)
        status_label = Label(
            text="[size=18][i]Progress: Page 1/2[/i][/size]",
            color=YELLOW,
            markup=True,
        )

        # update -->
        fullname = TextInput(hint_text="Full name", padding=[5, 5], multiline=False)
        about = TextInput(hint_text="About yourself", padding=[5, 5])
        # <-- update

        layout.add_widget(Image(source=str(logo_path)))
        layout.add_widget(title_label)
        layout.add_widget(fullname_label)
        layout.add_widget(fullname)  # <-- update
        layout.add_widget(about_label)
        layout.add_widget(about)  # <-- update
        layout.add_widget(status_label)

        return layout


ApplicationFormApp().run()
