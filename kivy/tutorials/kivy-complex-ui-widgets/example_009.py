from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.vkeyboard import VKeyboard


class VKeyboardApp(App):
    title = "VKeyboard Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (360, 640)

        root = BoxLayout(orientation="vertical")

        self.display_label = Label(text="Type in!", font_size=40)
        root.add_widget(self.display_label)

        # Create the virtual keyboard
        keyboard = VKeyboard(size_hint=(1, 0.4))
        keyboard.bind(on_key_up=self.keyboard_on_key_up)
        root.add_widget(keyboard)

        return root

    def keyboard_on_key_up(self, *args):
        keycode = args[1]
        text = args[2]
        if keycode == "backspace":
            if (
                len(self.display_label.text) > 0
                and self.display_label.text != "Type in!"
            ):
                self.display_label.text = self.display_label.text[:-1]
                if self.display_label.text == "":
                    self.display_label.text = "Type in!"
        elif keycode == "spacebar":
            if self.display_label.text == "Type in!":
                self.display_label.text = " "
            else:
                self.display_label.text += " "
        elif keycode in {"enter", "shift", "alt", "ctrl", "escape", "tab", "capslock"}:
            pass
        else:
            if self.display_label.text == "Type in!":
                self.display_label.text = text
            else:
                self.display_label.text += text


VKeyboardApp().run()
