from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class OnOffWidget(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name
        self.is_on = False

        self.name_label = QLabel(self.name)
        self.on_button = QPushButton("On")
        self.off_button = QPushButton("Off")

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.on_button)
        layout.addWidget(self.off_button)
        self.setLayout(layout)

        self.on_button.clicked.connect(self.on)
        self.off_button.clicked.connect(self.off)

        self.update_button_state()

    def on(self):
        self.is_on = True
        self.update_button_state()

    def off(self):
        self.is_on = False
        self.update_button_state()

    def update_button_state(self):
        if self.is_on:
            self.on_button.setStyleSheet("background-color: #4CAF50; color: #fff;")
            self.off_button.setStyleSheet("")
        else:
            self.on_button.setStyleSheet("")
            self.off_button.setStyleSheet("background-color: #D32F2F; color: #fff;")
