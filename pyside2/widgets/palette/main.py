import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from palette import PaletteGrid, PaletteHorizontal, PaletteVertical


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # PaletteGrid or PaletteHorizontal, or PaletteVertical
        palette = PaletteGrid("17undertones")
        palette.selected.connect(self.show_selected_color)
        self.setCentralWidget(palette)
        self.show()

    def show_selected_color(self, c):
        print("Selected: {}".format(c))


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()
