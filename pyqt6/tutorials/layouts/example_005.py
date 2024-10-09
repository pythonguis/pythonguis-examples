import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        layout = QGridLayout()

        layout.addWidget(Color("red"), 0, 3)
        layout.addWidget(Color("green"), 1, 1)
        layout.addWidget(Color("orange"), 2, 2)
        layout.addWidget(Color("blue"), 3, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
