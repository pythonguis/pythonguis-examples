import sys

from PySide6.QtWidgets import QApplication, QListWidget, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        listwidget = QListWidget()
        listwidget.addItems(["One", "Two", "Three"])

        # In QListWidget there are two separate signals for the item, and the str
        listwidget.currentItemChanged.connect(self.index_changed)
        listwidget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(listwidget)

    def index_changed(self, index):  # Not an index, index is a QListWidgetItem
        print(index.text())

    def text_changed(self, text):  # text is a str
        print(text)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
