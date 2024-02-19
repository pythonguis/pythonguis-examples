import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from colorbutton import ColorButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        palette = ColorButton(color="red")
        palette.colorChanged.connect(self.show_selected_color)
        self.setCentralWidget(palette)

    def show_selected_color(self, c):
        print("Selected: {}".format(c))


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()
