import json
from urllib.parse import urlencode

import constants
import requests
from PySide2.QtCore import (
    QObject,
    QRunnable,
    Signal,
    Slot,
)


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = Signal()
    error = Signal(str)
    result = Signal(dict, dict)


class WeatherWorker(QRunnable):
    """
    Worker thread for weather updates.
    """

    signals = WorkerSignals()
    is_interrupted = False

    def __init__(self, location):
        super().__init__()
        self.location = location

    @Slot()
    def run(self):
        try:
            params = dict(q=self.location, appid=constants.OPENWEATHERMAP_API_KEY)

            url = "http://api.openweathermap.org/data/2.5/weather?%s&units=metric" % urlencode(params)
            r = requests.get(url)
            weather = json.loads(r.text)

            # Check if we had a failure (the forecast will fail in the same way).
            if weather["cod"] != 200:
                raise Exception(weather["message"])

            url = "http://api.openweathermap.org/data/2.5/forecast?%s&units=metric" % urlencode(params)
            r = requests.get(url)
            forecast = json.loads(r.text)

            self.signals.result.emit(weather, forecast)

        except Exception as e:
            self.signals.error.emit(str(e))

        self.signals.finished.emit()
