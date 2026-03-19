from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("mainwindow.ui", self)

        self.plot(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Hours
            [30, 32, 34, 32, 33, 31, 29, 32, 35, 45],  # Degrees Celsius
        )

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)


app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec_()
