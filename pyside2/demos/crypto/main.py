import sys
from itertools import cycle

import constants
import numpy as np

# import requests_cache
from PySide2.QtCore import (
    Qt,
    QThreadPool,
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
    QMessageBox,
    QProgressBar,
    QTableView,
    QToolBar,
    QWidget,
)
from workers import UpdateWorker

color_cycle = cycle(constants.BREWER12PAIRED)
# requests_cache.install_cache('cache')

# Must be imported after PySide2.
import pyqtgraph as pg

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


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
        self.ax.setLabel("left", text="Rate")
        self.p1 = self.ax.getPlotItem()
        self.p1.scene().sigMouseMoved.connect(self.mouse_move_handler)

        # Add the right-hand axis for the market activity.
        self.p2 = pg.ViewBox()
        self.p2.enableAutoRange(axis=pg.ViewBox.XYAxes, enable=True)
        self.p1.showAxis("right")
        self.p1.scene().addItem(self.p2)
        self.p2.setXLink(self.p1)
        self.ax2 = self.p1.getAxis("right")
        self.ax2.linkToView(self.p2)
        self.ax2.setGrid(False)
        self.ax2.setLabel(text="Volume")

        self._market_activity = pg.PlotCurveItem(
            np.arange(constants.NUMBER_OF_TIMEPOINTS),
            np.arange(constants.NUMBER_OF_TIMEPOINTS),
            pen=pg.mkPen("k", style=Qt.PenStyle.DashLine, width=1),
        )
        self.p2.addItem(self._market_activity)

        # Automatically rescale our twinned Y axis.
        self.p1.vb.sigResized.connect(self.update_plot_scale)

        self.base_currency = constants.DEFAULT_BASE_CURRENCY

        # Store a reference to lines on the plot, and items in our
        # data viewer we can update rather than redraw.
        self._data_lines = dict()
        self._data_items = dict()
        self._data_colors = dict()
        self._data_visible = constants.DEFAULT_DISPLAY_CURRENCIES

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
        self.update_currency_list(constants.AVAILABLE_BASE_CURRENCIES)
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

    def get_or_create_data_row(self, currency):
        if currency not in self._data_items:
            self._data_items[currency] = self.add_data_row(currency)
        return self._data_items[currency]

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

    def mouse_move_handler(self, pos):
        pos = self.ax.getViewBox().mapSceneToView(pos)
        self.line.setPos(pos.x())
        self.update_data_viewer(int(pos.x()))

    def update_data_viewer(self, i):
        if i not in range(constants.NUMBER_OF_TIMEPOINTS):
            return

        for currency, data in self.data.items():
            self.update_data_row(currency, data[i])

    def update_data_row(self, currency, data):
        citem, vitem = self.get_or_create_data_row(currency)
        vitem.setText("%.4f" % data["close"])

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
        self.update_data_viewer(constants.NUMBER_OF_TIMEPOINTS - 1)

    def progress_callback(self, progress):
        self.progress.setValue(progress)

    def refresh_finished(self):
        self.worker = False
        self.redraw()

    def notify_error(self, error):
        e, tb = error
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(e.__class__.__name__)
        msg.setInformativeText(str(e))
        msg.setDetailedText(tb)
        msg.exec_()

    def update_plot_scale(self):
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())

    def redraw(self):
        y_min, y_max = sys.maxsize, 0
        x = np.arange(constants.NUMBER_OF_TIMEPOINTS)

        # Pre-process data into lists of x, y values.
        for currency, data in self.data.items():
            if data:
                _, close, high, low = zip(
                    *[(v["time"], v["close"], v["high"], v["low"]) for v in data]
                )

                if currency in self._data_visible:
                    # This line should be visible, if it's not drawn draw it.
                    if currency not in self._data_lines:
                        self._data_lines[currency] = {}
                        self._data_lines[currency]["high"] = self.ax.plot(
                            x,
                            high,  # Unpack a list of tuples into two lists, passed as individual args.
                            pen=pg.mkPen(
                                self.get_currency_color(currency),
                                width=2,
                                style=Qt.DotLine,
                            ),
                        )
                        self._data_lines[currency]["low"] = self.ax.plot(
                            x,
                            low,  # Unpack a list of tuples into two lists, passed as individual args.
                            pen=pg.mkPen(
                                self.get_currency_color(currency),
                                width=2,
                                style=Qt.DotLine,
                            ),
                        )
                        self._data_lines[currency]["close"] = self.ax.plot(
                            x,
                            close,  # Unpack a list of tuples into two lists, passed as individual args.
                            pen=pg.mkPen(
                                self.get_currency_color(currency),
                                width=3,
                            ),
                        )
                    else:
                        self._data_lines[currency]["high"].setData(x, high)
                        self._data_lines[currency]["low"].setData(x, low)
                        self._data_lines[currency]["close"].setData(x, close)

                    y_min, y_max = min(y_min, *low), max(y_max, *high)

                else:
                    # This line should not be visible, if it is delete it.
                    if currency in self._data_lines:
                        self._data_lines[currency]["high"].clear()
                        self._data_lines[currency]["low"].clear()
                        self._data_lines[currency]["close"].clear()

        self.ax.setLimits(yMin=y_min * 0.9, yMax=y_max * 1.1, xMin=min(x), xMax=max(x))

        self._market_activity.setData(x, self.volume)
        self.p2.setYRange(0, max(self.volume))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
