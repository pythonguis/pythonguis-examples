import pyqtgraph as pg
from PySide6.QtWidgets import QApplication

uiclass, baseclass = pg.Qt.loadUiType("mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plot(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Hours
            [30, 32, 34, 32, 33, 31, 29, 32, 35, 45],  # Degrees Celsius
        )

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
