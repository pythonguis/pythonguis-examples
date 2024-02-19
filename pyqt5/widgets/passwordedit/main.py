import sys

from password import PasswordEdit
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        password = PasswordEdit()
        self.setCentralWidget(password)


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()
