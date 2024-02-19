import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from paint import PaintWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        paint = PaintWidget(300, 300)
        paint.setPenWidth(5)
        paint.setPenColor("#EB5160")
        self.setCentralWidget(paint)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()
