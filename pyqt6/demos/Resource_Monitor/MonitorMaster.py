import sys
import time
import random
import colorsys
import math
import psutil

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import pyqtgraph as pg


class CPUWorker(QThread):
    cpu_data_updated = pyqtSignal(list)  # emits list of history lists

    def __init__(self, cpucount, history_length, parent=None):
        super().__init__(parent)
        self.cpucount = cpucount
        self.history_length = history_length
        self.cpu_history = [[] for _ in range(cpucount)]
        self.running = True

    def run(self):
        while self.running:
            speeds = psutil.cpu_percent(interval=1.0, percpu=True)
            for i in range(self.cpucount):
                self.cpu_history[i].append(speeds[i])
                if len(self.cpu_history[i]) > self.history_length:
                    self.cpu_history[i].pop(0)
            self.cpu_data_updated.emit(self.cpu_history)


class MemoryWorker(QThread):
    memory_data_updated = pyqtSignal(list, list, float, float)
    # emits mem_history, swap_history, current_available, current_swap_percent

    def __init__(self, history_length, parent=None):
        super().__init__(parent)
        self.history_length = history_length
        self.mem_history = []
        self.swap_history = []
        self.running = True

    def run(self):
        while self.running:
            time.sleep(0.1)
            vmem = psutil.virtual_memory()
            available = vmem.active / (1024 ** 3)
            swap = psutil.swap_memory().percent

            self.mem_history.append(available)
            self.swap_history.append(swap)
            if len(self.mem_history) > self.history_length:
                self.mem_history.pop(0)
            if len(self.swap_history) > self.history_length:
                self.swap_history.pop(0)
            self.memory_data_updated.emit(self.mem_history, self.swap_history, available, swap)


class NetworkWorker(QThread):
    network_data_updated = pyqtSignal(list, list, int, int)
    # emits upload_history, download_history, current_upload, current_download

    def __init__(self, history_length, parent=None):
        super().__init__(parent)
        self.history_length = history_length
        self.upload_history = []
        self.download_history = []
        self.running = True
        self.prev_net = psutil.net_io_counters()

    def run(self):
        while self.running:
            time.sleep(0.1)
            current_net = psutil.net_io_counters()
            upload_speed = current_net.bytes_sent - self.prev_net.bytes_sent
            download_speed = current_net.bytes_recv - self.prev_net.bytes_recv
            self.prev_net = current_net

            self.upload_history.append(upload_speed)
            self.download_history.append(download_speed)
            if len(self.upload_history) > self.history_length:
                self.upload_history.pop(0)
            if len(self.download_history) > self.history_length:
                self.download_history.pop(0)
            self.network_data_updated.emit(self.upload_history, self.download_history, upload_speed, download_speed)


class MonitorMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.cpucounts = psutil.cpu_count(logical=True)
        self.history_length = 100

        self.cpu_colors = self.generate_random_colors(self.cpucounts)
        self.setup_ui()
        self.setup_workers()

    def generate_random_colors(self, n):
        colors = []
        while len(colors) < n:
            h = random.random()
            s = random.uniform(0.6, 0.9)
            v = random.uniform(0.7, 1.0)
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            color = (int(r * 255), int(g * 255), int(b * 255))
            if color not in colors:
                colors.append(color)
        return colors

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)

        # --- CPU Plot Section ---
        cpu_heading = QLabel("CPU Usage")
        cpu_heading.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.main_layout.addWidget(cpu_heading)

        self.cpu_plot = pg.PlotWidget()
        self.main_layout.addWidget(self.cpu_plot)
        self.cpu_plot.setDisabled(True)

        self.cpu_curves = []
        for i in range(self.cpucounts):
            pen_color = pg.mkPen(color=self.cpu_colors[i], width=2)
            curve = self.cpu_plot.plot(pen=pen_color)
            self.cpu_curves.append(curve)

        self.colorGrid = QGridLayout()
        cols = 8
        for i in range(self.cpucounts):
            cpu_layout = QHBoxLayout()
            box = QLabel()
            box.setFixedSize(25, 25)
            color = self.cpu_colors[i]
            box.setStyleSheet("background-color: rgb({}, {}, {});".format(*color))
            label = QLabel(f"CPU {i}")
            cpu_layout.addWidget(box)
            cpu_layout.addWidget(label)
            container = QWidget()
            container.setLayout(cpu_layout)
            row = i // cols
            col = i % cols
            self.colorGrid.addWidget(container, row, col)
        self.main_layout.addLayout(self.colorGrid)

        # --- Memory Plot Section ---
        mem_heading = QLabel("Memory Resources")
        mem_heading.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.main_layout.addWidget(mem_heading)

        self.memory_plot = pg.PlotWidget()
        self.main_layout.addWidget(self.memory_plot)
        self.memory_plot.setDisabled(True)
        self.mem_curve = self.memory_plot.plot(pen=pg.mkPen(color='g', width=2))
        self.swap_curve = self.memory_plot.plot(pen=pg.mkPen(color='r', width=2))

        mem_legend_layout = QHBoxLayout()
        self.mem_label = QLabel("Memory Usage")
        self.mem_label.setStyleSheet("background-color: rgb(0, 254, 0); padding: 5px; color: black;")
        self.mem_label.setFixedSize(350, 30)
        mem_legend_layout.addWidget(self.mem_label)

        self.swap_label = QLabel("Swap Usage")
        self.swap_label.setStyleSheet("background-color: rgb(255, 0, 0); padding: 5px; color: black;")
        self.swap_label.setFixedSize(150, 30)
        mem_legend_layout.addWidget(self.swap_label)
        self.main_layout.addLayout(mem_legend_layout)

        # --- Network Plot Section ---
        net_heading = QLabel("Network Speed")
        net_heading.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.main_layout.addWidget(net_heading)

        self.network_plot = pg.PlotWidget()
        self.main_layout.addWidget(self.network_plot)
        self.network_plot.setDisabled(True)
        self.upload_curve = self.network_plot.plot(pen=pg.mkPen(color='b', width=2))
        self.download_curve = self.network_plot.plot(pen=pg.mkPen(color='r', width=2))

        net_legend_layout = QHBoxLayout()
        self.upload_label = QLabel("Upload")
        self.upload_label.setStyleSheet("background-color: rgb(0, 0, 255); padding: 5px;")
        self.upload_label.setFixedSize(250, 30)
        net_legend_layout.addWidget(self.upload_label)

        self.download_label = QLabel("Download")
        self.download_label.setStyleSheet("background-color: rgb(255, 0, 0); padding: 5px;")
        self.download_label.setFixedSize(250, 30)
        net_legend_layout.addWidget(self.download_label)
        self.main_layout.addLayout(net_legend_layout)

    def setup_workers(self):
        # CPU Worker
        self.cpu_worker = CPUWorker(self.cpucounts, self.history_length)
        self.cpu_worker.cpu_data_updated.connect(self.update_cpu_plot)
        self.cpu_worker.start()

        # Memory Worker
        self.memory_worker = MemoryWorker(self.history_length)
        self.memory_worker.memory_data_updated.connect(self.update_memory_plot)
        self.memory_worker.start()

        # Network Worker
        self.network_worker = NetworkWorker(self.history_length)
        self.network_worker.network_data_updated.connect(self.update_network_plot)
        self.network_worker.start()

    def update_cpu_plot(self, cpu_history):
        for i in range(self.cpucounts):
            self.cpu_curves[i].setData(cpu_history[i])
        self.cpu_plot.update()

    def update_memory_plot(self, mem_history, swap_history, current_available, current_swap):
        self.mem_curve.setData(x=list(range(len(mem_history))), y=mem_history)
        self.swap_curve.setData(x=list(range(len(swap_history))), y=swap_history)
        self.mem_label.setText(f"Active: {current_available:.1f} GB")
        self.swap_label.setText(f"Swap: {current_swap:.1f}%")
        self.memory_plot.update()

    def update_network_plot(self, upload_history, download_history, current_upload, current_download):
        self.upload_curve.setData(x=list(range(len(upload_history))), y=upload_history)
        self.download_curve.setData(x=list(range(len(download_history))), y=download_history)
        self.upload_label.setText(f"Upload: {current_upload} B/s")
        self.download_label.setText(f"Download: {current_download} B/s")
        self.network_plot.update()

    def closeEvent(self, event):
        # Stop threads when the window is closed
        self.cpu_worker.running = False
        self.memory_worker.running = False
        self.network_worker.running = False
        self.cpu_worker.quit()
        self.memory_worker.quit()
        self.network_worker.quit()
        self.cpu_worker.wait()
        self.memory_worker.wait()
        self.network_worker.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MonitorMaster()
    window.show()
    sys.exit(app.exec())
