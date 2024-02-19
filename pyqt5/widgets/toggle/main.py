from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from toggle import AnimatedToggle, Toggle


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        toggle_1 = Toggle()
        toggle_2 = AnimatedToggle(
            checked_color="#FFB000", pulse_checked_color="#44FFB000"
        )

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(toggle_1)
        layout.addWidget(toggle_2)
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication([])
w = Window()
w.show()
app.exec_()
