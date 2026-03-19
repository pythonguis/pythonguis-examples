from PyQt6 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI page
        uic.loadUi("mainwindow.ui", self)


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
