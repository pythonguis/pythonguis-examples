from datetime import datetime, timedelta, date
from itertools import cycle
import os
import sys
import traceback

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

import pyqtgraph as pg
import requests
import requests_cache

# CryptoCompare.com API Key
CRYPTOCOMPARE_API_KEY = ''

# Define a requests http cache to minimise API requests.
requests_cache.install_cache(os.path.expanduser('~/.goodforbitcoin'))

# Base currency is used to retrieve rates from bitcoinaverage.
DEFAULT_BASE_CURRENCY = 'USD'
AVAILABLE_BASE_CURRENCIES = ['USD', 'EUR', 'GBP']

# The crypto currencies to retrieve data about.
AVAILABLE_CRYPTO_CURRENCIES = ['BTC', 'ETH', 'LTC', 'EOS', 'XRP', 'BCH' ] #
DEFAULT_DISPLAY_CURRENCIES = ['BTC', 'ETH', 'LTC']

# Number of historic timepoints to plot (days).
NUMBER_OF_TIMEPOINTS = 150

# Colour cycle to use for plotting currencies.
BREWER12PAIRED = cycle(['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00',
                  '#cab2d6', '#6a3d9a', '#ffff99', '#b15928' ])

# Base PyQtGraph configuration.
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


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
        super(UpdateWorker, self).__init__()
        self.is_interrupted = False
        self.base_currency = base_currency
        self.signals.cancel.connect(self.cancel)

    @pyqtSlot()
    def run(self):
        auth_header = {
            'Apikey': CRYPTOCOMPARE_API_KEY
        }
        try:
            rates = {}
            for n, crypto in enumerate(AVAILABLE_CRYPTO_CURRENCIES, 1):
                url = 'https://min-api.cryptocompare.com/data/histoday?fsym={fsym}&tsym={tsym}&limit={limit}'
                r = requests.get(
                    url.format(**{
                        'fsym': crypto,
                        'tsym': self.base_currency,
                        'limit': NUMBER_OF_TIMEPOINTS-1,
                        'extraParams': 'www.learnpyqt.com',
                        'format': 'json',
                    }),
                    headers=auth_header,
                )
                r.raise_for_status()
                rates[crypto] = r.json().get('Data')

                self.signals.progress.emit(int(100 * n / len(AVAILABLE_CRYPTO_CURRENCIES)))

                if self.is_interrupted:
                    # Stop without emitting finish signals.
                    return

            url = 'https://min-api.cryptocompare.com/data/exchange/histoday?tsym={tsym}&limit={limit}'
            r = requests.get(
                url.format(**{
                    'tsym': self.base_currency,
                    'limit': NUMBER_OF_TIMEPOINTS-1,
                    'extraParams': 'www.learnpyqt.com',
                    'format': 'json',
                }),
                headers=auth_header,
            )
            r.raise_for_status()
            volume = [d['volume'] for d in r.json().get('Data')]

        except Exception as e:
            self.signals.error.emit((e, traceback.format_exc()))
            return

        self.signals.data.emit(rates, volume)
        self.signals.finished.emit()

    def cancel(self):
        self.is_interrupted = True


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QHBoxLayout()

        self.ax = pg.PlotWidget()
        self.ax.showGrid(True, True)

        self.line = pg.InfiniteLine(
            pos=-20,
            pen=pg.mkPen('k', width=3),
            movable=False  # We have our own code to handle dragless moving.
        )

        self.ax.addItem(self.line)
        self.ax.setLabel('left', text='Rate')
        self.p1 = self.ax.getPlotItem()
        self.p1.scene().sigMouseMoved.connect(self.mouse_move_handler)

        # Add the right-hand axis for the market activity.
        self.p2 = pg.ViewBox()
        self.p2.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)
        self.p1.showAxis('right')
        self.p1.scene().addItem(self.p2)
        self.p2.setXLink(self.p1)
        self.ax2 = self.p1.getAxis('right')
        self.ax2.linkToView(self.p2)
        self.ax2.setGrid(False)
        self.ax2.setLabel(text='Volume')

        self._market_activity = pg.PlotCurveItem(
            np.arange(NUMBER_OF_TIMEPOINTS), np.arange(NUMBER_OF_TIMEPOINTS),
            pen=pg.mkPen('k', style=Qt.DashLine, width=1)
        )
        self.p2.addItem(self._market_activity)

        # Automatically rescale our twinned Y axis.
        self.p1.vb.sigResized.connect(self.update_plot_scale)

        self.base_currency = DEFAULT_BASE_CURRENCY

        # Store a reference to lines on the plot, and items in our
        # data viewer we can update rather than redraw.
        self._data_lines = dict()
        self._data_items = dict()
        self._data_colors = dict()
        self._data_visible = DEFAULT_DISPLAY_CURRENCIES

        self.listView = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Currency", "Rate"])
        self.model.itemChanged.connect(self.check_check_state)

        self.listView.setModel(self.model)

        self.threadpool = QThreadPool()
        self.worker = False

        layout.addWidget(self.ax)
        layout.addWidget(self.listView)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.listView.setFixedSize(226, 400)
        self.setFixedSize(650, 400)

        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)
        self.currencyList = QComboBox()

        toolbar.addWidget(self.currencyList)
        self.update_currency_list(AVAILABLE_BASE_CURRENCIES)
        self.currencyList.setCurrentText(self.base_currency)
        self.currencyList.currentTextChanged.connect(self.change_base_currency)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        toolbar.addWidget(self.progress)

        self.refresh_historic_rates()
        self.setWindowTitle("Goodforbitcoin")
        self.show()

    def update_currency_list(self, currencies):
        for currency in currencies:
            self.currencyList.addItem(currency)

        self.currencyList.model().sort(0)

    def check_check_state(self, i):
        if not i.isCheckable():  # Skip data columns.
            return

        currency = i.text()
        checked = i.checkState() == Qt.Checked

        if currency in self._data_visible:
            if not checked:
                self._data_visible.remove(currency)
                self.redraw()
        else:
            if checked:
                self._data_visible.append(currency)
                self.redraw()

    def get_currency_color(self, currency):
        if currency not in self._data_colors:
            self._data_colors[currency] = next(BREWER12PAIRED)

        return self._data_colors[currency]

    def get_or_create_data_row(self, currency):
        if currency not in self._data_items:
            self._data_items[currency] = self.add_data_row(currency)
        return self._data_items[currency]

    def add_data_row(self, currency):
        citem = QStandardItem()
        citem.setText(currency)
        citem.setForeground(QBrush(QColor(
            self.get_currency_color(currency)
        )))
        citem.setColumnCount(2)
        citem.setCheckable(True)
        if currency in DEFAULT_DISPLAY_CURRENCIES:
            citem.setCheckState(Qt.Checked)

        vitem = QStandardItem()

        vitem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.model.setColumnCount(2)
        self.model.appendRow([citem, vitem])
        self.model.sort(0)
        return citem, vitem

    def mouse_move_handler(self, pos):
        pos = self.ax.getViewBox().mapSceneToView(pos)
        self.line.setPos(pos.x())
        self.update_data_viewer(int(pos.x()))

    def update_data_viewer(self, i):
        if i not in range(NUMBER_OF_TIMEPOINTS):
            return

        for currency, data in self.data.items():
            self.update_data_row(currency, data[i])

    def update_data_row(self, currency, data):
        citem, vitem = self.get_or_create_data_row(currency)
        vitem.setText("%.4f" % data['close'])

    def change_base_currency(self, currency):
        self.base_currency = currency
        self.refresh_historic_rates()

    def refresh_historic_rates(self):
        if self.worker:
            # If we have a current worker, send a kill signal
            self.worker.signals.cancel.emit()

        # Prefill our data store with None ('no data')
        self.data = {}
        self.volume = []

        self.worker = UpdateWorker(self.base_currency)
        # Handle callbacks with data and trigger refresh.
        self.worker.signals.data.connect(self.result_data_callback)
        self.worker.signals.finished.connect(self.refresh_finished)
        self.worker.signals.progress.connect(self.progress_callback)
        self.worker.signals.error.connect(self.notify_error)
        self.threadpool.start(self.worker)

    def result_data_callback(self, rates, volume):
        self.data = rates
        self.volume = volume
        self.redraw()
        self.update_data_viewer(NUMBER_OF_TIMEPOINTS-1)

    def progress_callback(self, progress):
        self.progress.setValue(progress)

    def refresh_finished(self):
        self.worker = False
        self.redraw()

    def notify_error(self, error):
        e, tb = error
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(e.__class__.__name__)
        msg.setInformativeText(str(e))
        msg.setDetailedText(tb)
        msg.exec_()

    def update_plot_scale(self):
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())

    def redraw(self):
        y_min, y_max = sys.maxsize, 0
        x = np.arange(NUMBER_OF_TIMEPOINTS)

        # Pre-process data into lists of x, y values.
        for currency, data in self.data.items():
            if data:
                _, close, high, low = zip(*[
                    (v['time'], v['close'], v['high'], v['low'])
                    for v in data
                ])

                if currency in self._data_visible:
                    # This line should be visible, if it's not drawn draw it.
                    if currency not in self._data_lines:
                        self._data_lines[currency] = {}
                        self._data_lines[currency]['high'] = self.ax.plot(
                            x, high,  # Unpack a list of tuples into two lists, passed as individual args.
                            pen=pg.mkPen(self.get_currency_color(currency), width=2, style=Qt.DotLine)
                        )
                        self._data_lines[currency]['low'] = self.ax.plot(
                            x, low,  # Unpack a list of tuples into two lists, passed as individual args.
                            pen=pg.mkPen(self.get_currency_color(currency), width=2, style=Qt.DotLine)
                        )
                        self._data_lines[currency]['close'] = self.ax.plot(
                            x, close,  # Unpack a list of tuples into two lists, passed as individual args.
                            pen=pg.mkPen(self.get_currency_color(currency), width=3)
                        )
                    else:
                        self._data_lines[currency]['high'].setData(x, high)
                        self._data_lines[currency]['low'].setData(x, low)
                        self._data_lines[currency]['close'].setData(x, close)

                    y_min, y_max = min(y_min, *low), max(y_max, *high)

                else:
                    # This line should not be visible, if it is delete it.
                    if currency in self._data_lines:
                        self._data_lines[currency]['high'].clear()
                        self._data_lines[currency]['low'].clear()
                        self._data_lines[currency]['close'].clear()

        self.ax.setLimits(yMin=y_min * 0.9, yMax=y_max * 1.1, xMin=min(x), xMax=max(x))

        self._market_activity.setData(x, self.volume)
        self.p2.setYRange(0, max(self.volume))


if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()