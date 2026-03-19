import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(204, 0, 0))  # r, g, b
        painter.setPen(pen)

        painter.drawEllipse(QtCore.QPoint(100, 100), 10, 10)
        painter.drawEllipse(QtCore.QPoint(100, 100), 15, 20)
        painter.drawEllipse(QtCore.QPoint(100, 100), 20, 30)
        painter.drawEllipse(QtCore.QPoint(100, 100), 25, 40)
        painter.drawEllipse(QtCore.QPoint(100, 100), 30, 50)
        painter.drawEllipse(QtCore.QPoint(100, 100), 35, 60)
        painter.end()
        self.label.setPixmap(canvas)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
