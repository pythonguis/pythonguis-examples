from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow

from datetime import datetime
import json
import os
import sys
import requests
from urllib.parse import urlencode

OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

"""
Get an API key from https://openweathermap.org/ to use with this
application.

"""

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.pushButton.pressed.connect(self.update_weather)
        self.pushButton.pressed.connect(self.update_forecast)

        self.show()

    def from_ts_to_time_of_day(self, ts):
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%I%p").lstrip("0")

    def update_weather(self):
        params = dict(
            q=self.lineEdit.text(),
            appid=OPENWEATHERMAP_API_KEY
        )

        url = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(params)
        r = requests.get(url)
        data = json.loads(r.text)

        self.latitudeLabel.setText("%.2f °" % data['coord']['lat'])
        self.longitudeLabel.setText("%.2f °" % data['coord']['lon'])

        self.windLabel.setText("%.2f m/s" % data['wind']['speed'])

        self.temperatureLabel.setText("%.1f °C" % data['main']['temp'])
        self.pressureLabel.setText("%d" % data['main']['pressure'])
        self.humidityLabel.setText("%d" % data['main']['humidity'])

        self.sunriseLabel.setText(self.from_ts_to_time_of_day(data['sys']['sunrise']))

        self.weatherLabel.setText("%s (%s)" % (
            data['weather'][0]['main'],
            data['weather'][0]['description']
        )
        )

        self.set_weather_icon(self.weatherIcon, data['weather'])

    def set_weather_icon(self, label, weather):
        label.setPixmap(
            QPixmap(os.path.join('images', "%s.png" %
                                 weather[0]['icon']
                                 )
                    )

        )

    def update_forecast(self):
        params = dict(
            q=self.lineEdit.text(),
            appid=OPENWEATHERMAP_API_KEY
        )

        url = 'http://api.openweathermap.org/data/2.5/forecast?%s&units=metric' % urlencode(params)
        r = requests.get(url)
        data = json.loads(r.text)

        for n, forecast in enumerate(data['list'][:5], 1):
            getattr(self, 'forecastTime%d' % n).setText(self.from_ts_to_time_of_day(forecast['dt']))
            self.set_weather_icon(getattr(self, 'forecastIcon%d' % n), forecast['weather'])
            getattr(self, 'forecastTemp%d' % n).setText("%.1f °C" % forecast['main']['temp'])

if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()