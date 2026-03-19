import sys

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            return  # Ignore the first time.

        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.drawLine(
            int(self.last_x),
            int(self.last_y),
            int(e.position().x()),
            int(e.position().y()),
        )
        painter.end()
        self.label.setPixmap(canvas)

        # Update the origin for next time.
        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
