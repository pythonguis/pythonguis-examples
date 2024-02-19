import traceback

import constants
import requests

# import requests_cache
from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)
    data = pyqtSignal(dict, list)
    cancel = pyqtSignal()


class UpdateWorker(QRunnable):
    """
    Worker thread for updating currency.
    """

    signals = WorkerSignals()

    def __init__(self, base_currency):
        super().__init__()
        self.is_interrupted = False
        self.base_currency = base_currency
        self.signals.cancel.connect(self.cancel)

    @pyqtSlot()
    def run(self):
        auth_header = {"Apikey": constants.CRYPTOCOMPARE_API_KEY}
        try:
            rates = {}
            for n, crypto in enumerate(constants.AVAILABLE_CRYPTO_CURRENCIES, 1):
                url = "https://min-api.cryptocompare.com/data/histoday?fsym={fsym}&tsym={tsym}&limit={limit}"
                r = requests.get(
                    url.format(
                        **{
                            "fsym": crypto,
                            "tsym": self.base_currency,
                            "limit": constants.NUMBER_OF_TIMEPOINTS - 1,
                            "extraParams": "www.pythonguis.com",
                            "format": "json",
                        }
                    ),
                    headers=auth_header,
                )
                r.raise_for_status()
                rates[crypto] = r.json().get("Data")

                self.signals.progress.emit(int(100 * n / len(constants.AVAILABLE_CRYPTO_CURRENCIES)))

                if self.is_interrupted:
                    # Stop without emitting finish signals.
                    return

            url = "https://min-api.cryptocompare.com/data/exchange/histoday?tsym={tsym}&limit={limit}"
            r = requests.get(
                url.format(
                    **{
                        "tsym": self.base_currency,
                        "limit": constants.NUMBER_OF_TIMEPOINTS - 1,
                        "extraParams": "www.pythonguis.com",
                        "format": "json",
                    }
                ),
                headers=auth_header,
            )
            r.raise_for_status()
            volume = [d["volume"] for d in r.json().get("Data")]

        except Exception as e:
            self.signals.error.emit((e, traceback.format_exc()))
            return

        self.signals.data.emit(rates, volume)
        self.signals.finished.emit()

    def cancel(self):
        self.is_interrupted = True
