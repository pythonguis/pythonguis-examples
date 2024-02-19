import sys
import time
import traceback
from collections import defaultdict
from datetime import date, datetime, timedelta
from itertools import cycle

import constants
import requests

# import requests_cache
from PySide2.QtCore import (
    QObject,
    QRunnable,
    Qt,
    QThreadPool,
    Signal,
    Slot,
)
from PySide2.QtGui import (
    QBrush,
    QColor,
    QStandardItem,
    QStandardItemModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QTableView,
    QToolBar,
    QWidget,
)

color_cycle = cycle(constants.BREWER12PAIRED)
# requests_cache.install_cache('cache')
# PyQtGraph must be imported after Qt.
import pyqtgraph as pg

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


# Build progressive request order, for filling up data
# Uses an depth-first search pattern, filling more recent data
# to a higher resolution more quickly with a
DATE_REQUEST_OFFSETS = [0]
current = [(0, constants.HISTORIC_DAYS_N)]
while current:
    a, b = current.pop(0)
    n = (a + b) // 2
    DATE_REQUEST_OFFSETS.append(n)

    if abs(a - n) > 1:
        current.insert(0, (a, n))

    if abs(b - n) > 1:
        current.append((b, n))


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = Signal()
    error = Signal(tuple)
    progress = Signal(int)
    data = Signal(int, dict)
    cancel = Signal()


class UpdateWorker(QRunnable):
    """
    Worker thread for updating currency.
    """

    signals = WorkerSignals()
    is_interrupted = False

    def __init__(self, base_currency):
        super().__init__()
        self.base_currency = base_currency
        self.signals.cancel.connect(self.cancel)

    @Slot()
    def run(self):
        try:
            today = date.today()
            total_requests = len(DATE_REQUEST_OFFSETS)

            for n, offset in enumerate(DATE_REQUEST_OFFSETS, 1):
                when = today - timedelta(days=offset)
                url = "http://api.fixer.io/{}".format(when.isoformat())
                r = requests.get(url, params={"base": self.base_currency})
                r.raise_for_status()
                data = r.json()
                rates = data["rates"]
                rates[self.base_currency] = 1.0

                self.signals.data.emit(offset, rates)
                self.signals.progress.emit(int(100 * n / total_requests))

                if not r.from_cache:
                    time.sleep(1)  # Don't be rude.

                if self.is_interrupted:
                    break

        except Exception as e:
            print(e)
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
            return

        self.signals.finished.emit()

    def cancel(self):
        self.is_interrupted = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.ax = pg.PlotWidget()
        self.ax.showGrid(True, True)

        self.line = pg.InfiniteLine(
            pos=-20,
            pen=pg.mkPen("k", width=3),
            movable=False,  # We have our own code to handle dragless moving.
        )

        self.ax.addItem(self.line)
        self.ax.setLimits(xMin=-constants.HISTORIC_DAYS_N + 1, xMax=0)
        self.ax.getPlotItem().scene().sigMouseMoved.connect(self.mouse_move_handler)

        self.base_currency = constants.DEFAULT_BASE_CURRENCY

        # Store a reference to lines on the plot, and items in our
        # data viewer we can update rather than redraw.
        self._data_lines = dict()
        self._data_items = dict()
        self._data_colors = dict()
        self._data_visible = constants.DEFAULT_DISPLAY_CURRENCIES

        self._last_updated = None

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
        self.update_currency_list(constants.DEFAULT_DISPLAY_CURRENCIES)
        self.currencyList.setCurrentText(self.base_currency)
        self.currencyList.currentTextChanged.connect(self.change_base_currency)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        toolbar.addWidget(self.progress)

        self.refresh_historic_rates()
        self.setWindowTitle("Doughnut")
        self.show()

    def update_currency_list(self, currencies):
        for currency in currencies:
            if self.currencyList.findText(currency) == -1:
                self.currencyList.addItem(currency)

        self.currencyList.model().sort(0)

    def check_check_state(self, i):
        if not i.isCheckable():  # Skip data columns.
            return

        currency = i.text()
        checked = i.checkState() == Qt.CheckState.Checked

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
            self._data_colors[currency] = next(color_cycle)

        return self._data_colors[currency]

    def add_data_row(self, currency):
        citem = QStandardItem()
        citem.setText(currency)
        citem.setForeground(QBrush(QColor(self.get_currency_color(currency))))
        citem.setColumnCount(2)
        citem.setCheckable(True)
        if currency in constants.DEFAULT_DISPLAY_CURRENCIES:
            citem.setCheckState(Qt.CheckState.Checked)

        vitem = QStandardItem()

        vitem.setTextAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.model.setColumnCount(2)
        self.model.appendRow([citem, vitem])
        self.model.sort(0)
        return citem, vitem

    def get_or_create_data_row(self, currency):
        if currency not in self._data_items:
            self._data_items[currency] = self.add_data_row(currency)
        return self._data_items[currency]

    def mouse_move_handler(self, pos):
        pos = self.ax.getViewBox().mapSceneToView(pos)
        self.line.setPos(pos.x())
        self.update_data_viewer(int(pos.x()))

    def update_data_row(self, currency, value):
        citem, vitem = self.get_or_create_data_row(currency)
        vitem.setText("%.4f" % value)

    def update_data_viewer(self, d):
        try:
            data = self.data[d]
        except IndexError:  # Skip update if out of bounds.
            return

        if not data:  # Skip update if we have no data.
            return

        for k, v in data.items():
            self.update_data_row(k, v)

    def change_base_currency(self, currency):
        self.base_currency = currency
        self.refresh_historic_rates()

    def refresh_historic_rates(self):
        if self.worker:
            # If we have a current worker, send a kill signal
            self.worker.signals.cancel.emit()

        # Prefill our data store with None ('no data')
        self.data = [None] * constants.HISTORIC_DAYS_N

        self.worker = UpdateWorker(self.base_currency)
        # Handle callbacks with data and trigger refresh.
        self.worker.signals.data.connect(self.result_data_callback)
        self.worker.signals.finished.connect(self.refresh_finished)
        self.worker.signals.progress.connect(self.progress_callback)
        self.threadpool.start(self.worker)

    def result_data_callback(self, n, rates):
        self.data[n] = rates

        # Refresh plot if we haven't for >1 second.
        if (
            self._last_updated is None
            or self._last_updated < datetime.now() - timedelta(seconds=1)
        ):
            self.redraw()
            self._last_updated = datetime.now()

    def progress_callback(self, progress):
        self.progress.setValue(progress)

    def refresh_finished(self):
        self.worker = False
        self.redraw()
        # Ensure all currencies we know about are in the dropdown list now.
        self.update_currency_list(self._data_items.keys())

    def redraw(self):
        """
        Process data from store and prefer to draw.
        :return:
        """
        today = date.today()
        plotd = defaultdict(list)
        x_ticks = []

        tick_step_size = constants.HISTORIC_DAYS_N / 6
        # Pre-process data into lists of x, y values
        for n, data in enumerate(self.data):
            if data:
                for currency, v in data.items():
                    plotd[currency].append((-n, v))

            when = today - timedelta(days=n)
            if (n - tick_step_size // 2) % tick_step_size == 0:
                x_ticks.append((-n, when.strftime("%d-%m")))

        # Update the plot
        keys = sorted(plotd.keys())
        y_min, y_max = sys.maxsize, 0

        for currency in keys:
            x, y = zip(*plotd[currency])

            if currency in self._data_visible:
                y_min = min(y_min, *y)
                y_max = max(y_max, *y)
            else:
                x, y = [], []

            if currency in self._data_lines:
                self._data_lines[currency].setData(x, y)
            else:
                self._data_lines[currency] = self.ax.plot(
                    x,
                    y,  # Unpack a list of tuples into two lists, passed as individual args.
                    pen=pg.mkPen(self.get_currency_color(currency), width=2),
                )

        self.ax.setLimits(yMin=y_min * 0.9, yMax=y_max * 1.1)
        self.ax.getAxis("bottom").setTicks([x_ticks, []])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
