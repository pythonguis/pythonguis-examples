from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class OnOffWidget(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name  # Name of widget used for searching
        self.is_on = False  # Current state (true=ON, false=OFF)

        self.name_label = QLabel(self.name)  #  The widget label
        self.on_button = QPushButton("On")  # The ON button
        self.off_button = QPushButton("Off")  # The OFF button

        layout = QHBoxLayout()  # A horizontal layout to encapsulate the above
        layout.addWidget(self.name_label)  # Add the label to the layout
        layout.addWidget(self.on_button)  # Add the ON button to the layout
        layout.addWidget(self.off_button)  # Add the OFF button to the layout
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
            self.off_button.setStyleSheet("background-color: none; color: none;")
        else:
            self.on_button.setStyleSheet("background-color: none; color: none;")
            self.off_button.setStyleSheet("background-color: #D32F2F; color: #fff;")
