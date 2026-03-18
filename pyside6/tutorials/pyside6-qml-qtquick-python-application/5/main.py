import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer

from time import strftime, localtime

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('main.qml')

def update_time():
    # Pass the current time to QML.
    curr_time = strftime("%H:%M:%S", localtime())
    engine.rootObjects()[0].setProperty('currTime', curr_time)

timer = QTimer()
timer.setInterval(100)  # msecs 100 = 1/10th sec
timer.timeout.connect(update_time)
timer.start()

update_time() # initial startup

sys.exit(app.exec_())