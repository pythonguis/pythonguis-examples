import sys

from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        combobox = QComboBox()
        combobox.addItems(["One", "Two", "Three"])

        # The default signal from currentIndexChanged sends the index
        combobox.currentIndexChanged.connect(self.index_changed)

        # The same signal can send a text string
        combobox.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(combobox)

    def index_changed(self, index):  # index is an int stating from 0
        print(index)

    def text_changed(self, text):  # text is a str
        print(text)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
