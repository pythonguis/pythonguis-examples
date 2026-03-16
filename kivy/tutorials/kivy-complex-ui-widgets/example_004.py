from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView


class FileChooserApp(App):
    title = "FileChooser Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (360, 640)

        root = BoxLayout(orientation="vertical")

        # Create icon-view and list-view file choosers
        filechooser_icons = FileChooserIconView()
        filechooser_list = FileChooserListView()

        root.add_widget(filechooser_icons)
        root.add_widget(filechooser_list)

        return root


FileChooserApp().run()
