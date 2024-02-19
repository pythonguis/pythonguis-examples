import random
import sys
import time

from constants import (
    IMG_BOMB,
    IMG_CLOCK,
    LEVELS,
    STATUS_ICONS,
    Status,
)
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from widgets import PositionSquare


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.b_size, self.n_mines = LEVELS[1]

        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.clock = QLabel()
        self.clock.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(QFont.Weight.Thin)
        self.mines.setFont(f)
        self.clock.setFont(f)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        self.mines.setText("%03d" % self.n_mines)
        self.clock.setText("000")

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smiley.png"))
        self.button.setFlat(True)

        self.button.pressed.connect(self.button_pressed)

        label = QLabel()
        label.setPixmap(QPixmap.fromImage(IMG_BOMB))
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        hb.addWidget(label)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        label = QLabel()
        label.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hb.addWidget(label)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.init_map()
        self.update_status(Status.READY)

        self.reset_map()
        self.update_status(Status.READY)

        self.setWindowTitle("Moonsweeper")

        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = PositionSquare(x, y)
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
                w.clicked.connect(self.trigger_start)
                w.expandable.connect(self.expand_reveal)
                w.ohno.connect(self.game_over)

    def reset_map(self):
        # Clear all mine positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()

        # Add mines to the positions
        positions = []
        while len(positions) < self.n_mines:
            x, y = (
                random.randint(0, self.b_size - 1),
                random.randint(0, self.b_size - 1),
            )
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        def get_adjacency_n(x, y):
            positions = self.get_surrounding(x, y)
            n_mines = sum(1 if w.is_mine else 0 for w in positions)

            return n_mines

        # Add adjacencies to the positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.adjacent_n = get_adjacency_n(x, y)

        # Place starting marker
        while True:
            x, y = (
                random.randint(0, self.b_size - 1),
                random.randint(0, self.b_size - 1),
            )
            w = self.grid.itemAtPosition(y, x).widget()
            # We don't want to start on a mine.
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_start = True

                # Reveal all positions around this, if they are not mines either.
                for w in self.get_surrounding(x, y):
                    if not w.is_mine:
                        w.click()
                break

    def get_surrounding(self, x, y):
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions

    def button_pressed(self):
        if self.status == Status.FAILED:
            self.update_status(Status.FAILED)
            self.reveal_map()

        elif self.status == Status.FAILED:
            self.update_status(Status.READY)
            self.reset_map()

    def reveal_map(self):
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reveal()

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def trigger_start(self, *args):
        if self.status != Status.PLAYING:
            # First click.
            self.update_status(Status.PLAYING)
            # Start timer.
            self._timer_start_nsecs = int(time.time())

    def update_status(self, status):
        self.status = status
        self.button.setIcon(QIcon(STATUS_ICONS[self.status]))

    def update_timer(self):
        if self.status == Status.PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)

    def game_over(self):
        self.reveal_map()
        self.update_status(Status.FAILED)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
