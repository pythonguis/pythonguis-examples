# Basic Kivy Widgets
# https://www.pythonguis.com/tutorials/kivy-ux-widgets/

from pathlib import Path

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton  # <-- update

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
        fullname = TextInput(hint_text="Full name", padding=[5, 5], multiline=False)
        about = TextInput(hint_text="About yourself", padding=[5, 5])
        save_progress = Label(text="Save progress?", font_size=18, color=YELLOW)
        save_checkbox = CheckBox(active=False)
        h_layout = BoxLayout(padding=[0, 5])
        h_layout.add_widget(save_progress)
        h_layout.add_widget(save_checkbox)

        # update -->
        toggle = ToggleButton(text="Yes")
        h_layout.add_widget(toggle)
        # <-- update

        layout.add_widget(Image(source=str(logo_path)))
        layout.add_widget(title_label)
        layout.add_widget(fullname_label)
        layout.add_widget(fullname)
        layout.add_widget(about_label)
        layout.add_widget(about)
        layout.add_widget(h_layout)
        layout.add_widget(status_label)

        return layout


ApplicationFormApp().run()
