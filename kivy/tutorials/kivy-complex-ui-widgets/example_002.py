from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner


class SpinnerApp(App):
    title = "Spinner Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (300, 300)

        root = FloatLayout()

        # Create the Spinner
        spinner = Spinner(
            text="Home",
            values=("Home", "Latest", "FAQ", "Forum", "Contact", "About"),
            size_hint=(None, None),
            size=(200, 70),
            pos_hint={"center_x": 0.2, "center_y": 0.9},
            sync_height=True,
        )

        root.add_widget(spinner)

        return root


SpinnerApp().run()
