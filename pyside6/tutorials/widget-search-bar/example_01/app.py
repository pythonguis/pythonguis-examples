from customwidgets import OnOffWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle("Control Panel")

        container = QWidget()
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)
        self.setCentralWidget(container)

        onoff = OnOffWidget("Stove")
        container_layout.addWidget(onoff)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
