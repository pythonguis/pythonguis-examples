# Getting Started With Kivy for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-kivy/

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

ROWS = COLS = 3


class GridApp(App):
    def build(self):
        root = GridLayout(rows=ROWS, cols=COLS)
        for i in range(ROWS):
            for j in range(COLS):
                root.add_widget(Button(text=f"({i}, {j})"))
        return root


GridApp().run()
