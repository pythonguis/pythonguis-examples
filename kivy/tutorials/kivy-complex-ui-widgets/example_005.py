from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class PopupApp(App):
    title = "Popup Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (400, 400)

        root = FloatLayout()

        button = Button(
            text="Open Popup",
            on_press=lambda x: self.show_popup(),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        root.add_widget(button)

        return root

    def show_popup(self):
        # Create and show the Popup
        popup = Popup(
            title="Info",
            size_hint=(0.6, 0.6),
            size=(300, 300),
            auto_dismiss=False,
        )

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        message = Label(text="Hello, World!")

        ok_button = Button(text="OK", size_hint=(None, None), size=(80, 40))
        ok_button.bind(on_release=popup.dismiss)

        layout.add_widget(message)
        layout.add_widget(ok_button)

        popup.content = layout
        popup.open()


PopupApp().run()
