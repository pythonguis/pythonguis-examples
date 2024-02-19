import os
import sys

from MainWindow import Ui_MainWindow
from PyQt5.QtCore import (
    QThreadPool,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)
from utils import from_ts_to_time_of_day
from workers import WeatherWorker

"""
Get an API key from https://openweathermap.org/ to use with this
application. Add it in constants.py or set the OPENWEATHERMAP_API_KEY environment
variable before running this script.
"""


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.update_weather)

        self.threadpool = QThreadPool()

        self.show()

    def alert(self, message):
        QMessageBox.warning(self, "Warning", message)

    def update_weather(self):
        worker = WeatherWorker(self.lineEdit.text())
        worker.signals.result.connect(self.weather_result)
        worker.signals.error.connect(self.alert)
        self.threadpool.start(worker)

    def weather_result(self, weather, forecasts):
        self.latitudeLabel.setText("%.2f °" % weather["coord"]["lat"])
        self.longitudeLabel.setText("%.2f °" % weather["coord"]["lon"])

        self.windLabel.setText("%.2f m/s" % weather["wind"]["speed"])

        self.temperatureLabel.setText("%.1f °C" % weather["main"]["temp"])
        self.pressureLabel.setText("%d" % weather["main"]["pressure"])
        self.humidityLabel.setText("%d" % weather["main"]["humidity"])

        self.sunriseLabel.setText(from_ts_to_time_of_day(weather["sys"]["sunrise"]))

        self.weatherLabel.setText(
            "%s (%s)"
            % (
                weather["weather"][0]["main"],
                weather["weather"][0]["description"],
            )
        )

        self.set_weather_icon(self.weatherIcon, weather["weather"])

        for n, forecast in enumerate(forecasts["list"][:5], 1):
            getattr(self, "forecastTime%d" % n).setText(from_ts_to_time_of_day(forecast["dt"]))
            self.set_weather_icon(getattr(self, "forecastIcon%d" % n), forecast["weather"])
            getattr(self, "forecastTemp%d" % n).setText("%.1f °C" % forecast["main"]["temp"])

    def set_weather_icon(self, label, weather):
        label.setPixmap(QPixmap(os.path.join("images", "%s.png" % weather[0]["icon"])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
