from customwidgets import OnOffWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle("Control Panel")

        container = QWidget()
        containerLayout = QVBoxLayout()
        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        onoff = OnOffWidget("Stove")
        containerLayout.addWidget(onoff)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
