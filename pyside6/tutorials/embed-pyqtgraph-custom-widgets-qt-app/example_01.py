import pyqtgraph as pg
from PySide6.QtWidgets import QApplication

uiclass, baseclass = pg.Qt.loadUiType("mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
