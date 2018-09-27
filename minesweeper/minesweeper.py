from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
import time
import sys

IMG_BOMB = QImage("./images/bug.png")
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/clock-select.png")

NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}

LEVELS = [
    (8, 10),
    (16, 40),
    (24, 99)
]

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

STATUS_ICONS = {
    STATUS_READY: "./images/plus.png",
    STATUS_PLAYING: "./images/smiley.png",
    STATUS_FAILED: "./images/cross.png",
    STATUS_SUCCESS: "./images/smiley-lol.png",
}


class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    expandable_safe = pyqtSignal(int, int)
    clicked = pyqtSignal()
    flagged = pyqtSignal(bool)
    ohno = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False
        self.is_end = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
            if self.is_end:
                inner = NUM_COLORS[1]
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            elif self.adjacent_n > 0:
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMG_FLAG))

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged
        self.update()
        self.flagged.emit(self.is_flagged)

    def reveal_self(self):
        self.is_revealed = True
        self.update()

    def reveal(self):
        if not self.is_revealed:
            self.reveal_self()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

            if self.is_mine:
                self.is_end = True
                self.ohno.emit()

    def click(self):
        if not self.is_revealed and not self.is_flagged:
            self.reveal()

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
        if e.button() == Qt.RightButton:
            if not self.is_revealed:
                self.toggle_flag()
            else:
                self.expandable_safe.emit(self.x, self.y)

        elif e.button() == Qt.LeftButton:
            self.click()
        self.clicked.emit()



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        app = QApplication.instance()
        app_args = app.arguments()
        
        self.level = int(app_args[1]) if len(app_args) == 2 and app_args[1].isnumeric() else 1
        if self.level < 0 or self.level > len(LEVELS):
            raise ValueError('level out of bounds')
        self.b_size, self.n_mines = LEVELS[self.level]

        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.mines.setFont(f)
        self.clock.setFont(f)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)
        self._timer.start(1000)  # 1 second timer

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smiley.png"))
        self.button.setFlat(True)

        self.button.pressed.connect(self.button_pressed)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hb.addWidget(l)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        l.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hb.addWidget(l)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.init_map()
        self.update_status(STATUS_READY)

        self.reset_map()
        self.update_status(STATUS_READY)

        self.setWindowTitle("Minesweeper")
        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = Pos(x, y)
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
                w.clicked.connect(self.trigger_start)
                w.expandable.connect(self.expand_reveal)
                w.expandable_safe.connect(self.expand_reveal_if_looks_safe)
                w.flagged.connect(self.flag_toggled)
                w.ohno.connect(self.game_over)

    def reset_map(self):
        self.n_mines = LEVELS[self.level][1]
        self.mines.setText("%03d" % self.n_mines)
        self.clock.setText("000")
        
        # Clear all mine positions
        for _, _, w in self.get_all():
            w.reset()

        # Add mines to the positions
        positions = []
        while len(positions) < self.n_mines:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        def get_adjacency_n(x, y):
            positions = [w for _, _, w in self.get_surrounding(x, y)]
            n_mines = sum(1 if w.is_mine else 0 for w in positions)

            return n_mines

        # Add adjacencies to the positions
        for x, y, w in self.get_all():
            w.adjacent_n = get_adjacency_n(x, y)

        # Place starting marker
        while True:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            w = self.grid.itemAtPosition(y, x).widget()
            # We don't want to start on a mine.
            if (x, y) not in positions:
                w.is_start = True

                # Reveal all positions around this, if they are not mines either.
                for _, _, w in self.get_surrounding(x, y):
                    if not w.is_mine:
                        w.click()
                break

    def get_all(self):
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                yield (x, y, self.grid.itemAtPosition(y, x).widget())

    def get_surrounding(self, x, y):
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append((xi, yi, self.grid.itemAtPosition(yi, xi).widget()))

        return positions

    def button_pressed(self):
        if self.status == STATUS_PLAYING:
            self.update_status(STATUS_FAILED)
            self.reveal_map()

        elif self.status in (STATUS_FAILED, STATUS_SUCCESS):
            self.update_status(STATUS_READY)
            self.reset_map()

    def reveal_map(self):
        for _, _, w in self.get_all():
            w.reveal_self()

    def get_revealable_around(self, x, y, force=False):
        for xi, yi, w in self.get_surrounding(x, y):
            if (force or not w.is_mine) and not w.is_flagged:
                yield (xi, yi, w)

    def expand_reveal(self, x, y, force=False):
        for _, _, w in self.get_revealable_around(x, y, force):
            w.reveal()

    def determine_revealable_around_looks_safe(self, x, y, existing):
        flagged_count = 0
        for _, _, w in self.get_surrounding(x, y):
            if w.is_flagged:
                flagged_count += 1
        w = self.grid.itemAtPosition(y, x).widget()
        if flagged_count == w.adjacent_n:
            for xi, yi, w in self.get_revealable_around(x, y, True):
                if (xi, yi) not in ((xq, yq) for xq, yq, _ in existing):
                    existing.append((xi, yi, w))
                    self.determine_revealable_around_looks_safe(xi, yi, existing)

    def expand_reveal_if_looks_safe(self, x, y):
        reveal = []
        self.determine_revealable_around_looks_safe(x, y, reveal)
        for _, _, w in reveal:
            w.reveal()

    def trigger_start(self, *args):
        if self.status == STATUS_READY:
            # First click.
            self.update_status(STATUS_PLAYING)
            # Start timer.
            self._timer_start_nsecs = int(time.time())
        elif self.status == STATUS_PLAYING:
            self.check_win_condition()

    def update_status(self, status):
        self.status = status
        self.button.setIcon(QIcon(STATUS_ICONS[self.status]))

    def update_timer(self):
        if self.status == STATUS_PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)

    def game_over(self):
        self.reveal_map()
        self.update_status(STATUS_FAILED)

    def flag_toggled(self, flagged):
        adjustment = -1 if flagged else 1
        self.n_mines += adjustment
        self.mines.setText("%03d" % self.n_mines)
        #self.check_win_condition()

    def check_win_condition(self):
        if self.n_mines == 0:
            if all(w.is_revealed or w.is_flagged for _, _, w in self.get_all()):
                self.update_status(STATUS_SUCCESS)
        # TODO: if the only unrevealed squares are mines, then no need to flag them, the player wins


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
