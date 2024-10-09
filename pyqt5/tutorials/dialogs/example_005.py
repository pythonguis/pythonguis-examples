import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        button = QMessageBox.question(
            self,
            "Question dialog",
            "The longer message",
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Yes!")
        else:
            print("No!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
