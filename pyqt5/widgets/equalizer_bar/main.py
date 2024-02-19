import random
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from equalizer_bar import EqualizerBar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.equalizer = EqualizerBar(
            5,
            [
                "#0C0786",
                "#40039C",
                "#6A00A7",
                "#8F0DA3",
                "#B02A8F",
                "#CA4678",
                "#E06461",
                "#F1824C",
                "#FCA635",
                "#FCCC25",
                "#EFF821",
            ],
        )
        self.equalizer.setBarSolidYPercent(0.4)
        # self.equalizer.setBarSolidXPercent(0.4)
        self.setCentralWidget(self.equalizer)

        self._timer = QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.update_values)
        self._timer.start()

    def update_values(self):
        self.equalizer.setValues(
            [
                min(100, v + random.randint(0, 50) if random.randint(0, 5) > 2 else v)
                for v in self.equalizer.values()
            ]
        )


app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()
