import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from time import strftime, localtime

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('main.qml')

# Pass the current time to QML.
curr_time = strftime("%H:%M:%S", localtime())
engine.rootObjects()[0].setProperty('currTime', curr_time)

sys.exit(app.exec())