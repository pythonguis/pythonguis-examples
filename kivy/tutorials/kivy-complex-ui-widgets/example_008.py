from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader


class TabbedPanelApp(App):
    title = "TabbedPanel Widget"

    def build(self):
        Window.clearcolor = (0, 0.31, 0.31, 1.0)
        Window.size = (360, 640)

        # Create the TabbedPanel
        root = TabbedPanel(do_default_tab=False)

        # Create the tabs
        general_tab = TabbedPanelHeader(text="General")
        general_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        general_content.add_widget(Label(text="General Settings", font_size=40))
        general_tab.content = general_content
        root.add_widget(general_tab)

        editor_tab = TabbedPanelHeader(text="Editor")
        editor_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        editor_content.add_widget(Label(text="Editor Settings", font_size=40))
        editor_tab.content = editor_content
        root.add_widget(editor_tab)

        profile_tab = TabbedPanelHeader(text="Profile")
        profile_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        profile_content.add_widget(Label(text="User Profile", font_size=40))
        profile_tab.content = profile_content
        root.add_widget(profile_tab)

        return root


TabbedPanelApp().run()
