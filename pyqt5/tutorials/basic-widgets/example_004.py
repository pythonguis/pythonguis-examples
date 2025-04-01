import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QLabel()
        widget.setPixmap(QPixmap("otje.jpg"))
        widget.setScaledContents(True)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(widget)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
