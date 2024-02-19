from constants import (
    IMG_BOMB,
    IMG_FLAG,
    IMG_START,
    NUM_COLORS,
)
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QPainter,
    QPalette,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QWidget


class PositionSquare(QWidget):
    expandable = Signal(int, int)
    clicked = Signal()
    ohno = Signal()

    def __init__(self, x, y):
        super().__init__()

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.ColorRole.Window)
            outer, inner = color, color
        else:
            outer, inner = Qt.GlobalColor.gray, Qt.GlobalColor.lightGray

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
                p.drawText(
                    r,
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                    str(self.adjacent_n),
                )

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMG_FLAG))

    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton and not self.is_revealed:
            self.flag()

        elif e.button() == Qt.MouseButton.LeftButton:
            self.click()

            if self.is_mine:
                self.ohno.emit()
