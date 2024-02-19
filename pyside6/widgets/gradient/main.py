import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from gradient import Gradient


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        gradient = Gradient()
        gradient.setGradient([(0, "black"), (1, "green"), (0.5, "red")])
        self.setCentralWidget(gradient)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec()
