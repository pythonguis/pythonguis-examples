from customwidgets import OnOffWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCompleter,
    QLineEdit,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle("Control Panel")

        # Control widgets
        controls = QWidget()
        controls_layout = QVBoxLayout()
        devices = [
            "Heater",
            "Stove",
            "Living Room Light",
            "Balcony Light",
            "Fan",
            "Room Light",
            "Oven",
            "Desk Light",
            "Bedroom Heater",
            "Wall Switch",
        ]
        self.widgets = []
        for device in devices:
            switch = OnOffWidget(device)
            controls_layout.addWidget(switch)
            self.widgets.append(switch)

        spacer = QSpacerItem(
            1,
            1,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding,
        )
        controls_layout.addItem(spacer)
        controls.setLayout(controls_layout)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(controls)

        # Search bar
        searchbar = QLineEdit(placeholderText="Search devices...")
        searchbar.textChanged.connect(self.update_display)

        # Adding text completer
        completer = QCompleter(devices)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        searchbar.setCompleter(completer)

        # Main container
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(searchbar)
        container_layout.addWidget(scroll_area)
        container.setLayout(container_layout)
        self.setCentralWidget(container)

    def update_display(self, text):
        search = text.strip().casefold()
        for widget in self.widgets:
            if widget.name.casefold().startswith(search):
                widget.show()
            else:
                widget.hide()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
