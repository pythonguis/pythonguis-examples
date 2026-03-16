# Basic Kivy Widgets
# https://www.pythonguis.com/tutorials/kivy-ux-widgets/

from kivy.app import App
from kivy.uix.video import Video


class MainApp(App):
    def build(self):
        player = Video(source="sample-video.mp4", state="play")
        return player


MainApp().run()
