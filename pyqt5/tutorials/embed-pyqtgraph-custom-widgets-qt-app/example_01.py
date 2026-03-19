from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("mainwindow.ui", self)


app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec_()
