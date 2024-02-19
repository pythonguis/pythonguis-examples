from PyQt5.QtCore import QRect, QRectF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QLinearGradient, QPainter, QPen
from PyQt5.QtWidgets import QColorDialog, QSizePolicy, QWidget


class Gradient(QWidget):
    gradientChanged = pyqtSignal()

    def __init__(self, gradient=None):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        if gradient:
            self._gradient = gradient

        else:
            self._gradient = [
                (0.0, "#000000"),
                (1.0, "#ffffff"),
            ]

        # Stop point handle sizes.
        self._handle_w = 10
        self._handle_h = 10

        self._drag_position = None

    def paintEvent(self, e):
        painter = QPainter(self)
        width = painter.device().width()
        height = painter.device().height()

        # Draw the linear horizontal gradient.
        gradient = QLinearGradient(0, 0, width, 0)
        for stop, color in self._gradient:
            gradient.setColorAt(stop, QColor(color))

        rect = QRect(0, 0, width, height)
        painter.fillRect(rect, gradient)

        pen = QPen()

        y = painter.device().height() / 2

        # Draw the stop handles.
        for stop, _ in self._gradient:
            pen.setColor(QColor("white"))
            painter.setPen(pen)

            painter.drawLine(
                int(stop * width),
                int(y - self._handle_h),
                int(stop * width),
                int(y + self._handle_h),
            )

            pen.setColor(QColor("red"))
            painter.setPen(pen)

            rect = QRectF(
                stop * width - self._handle_w / 2,
                y - self._handle_h / 2,
                self._handle_w,
                self._handle_h,
            )
            painter.drawRect(rect)

        painter.end()

    def sizeHint(self):
        return QSize(200, 50)

    def _sort_gradient(self):
        self._gradient = sorted(self._gradient, key=lambda g: g[0])

    def _constrain_gradient(self):
        self._gradient = [
            # Ensure values within valid range.
            (max(0.0, min(1.0, stop)), color)
            for stop, color in self._gradient
        ]

    def setGradient(self, gradient):
        assert all([0.0 <= stop <= 1.0 for stop, _ in gradient])
        self._gradient = gradient
        self._constrain_gradient()
        self._sort_gradient()
        self.gradientChanged.emit()

    def gradient(self):
        return self._gradient

    @property
    def _end_stops(self):
        return [0, len(self._gradient) - 1]

    def addStop(self, stop, color=None):
        # Stop is a value 0...1, find the point to insert this stop
        # in the list.
        assert 0.0 <= stop <= 1.0

        for n, g in enumerate(self._gradient):
            if g[0] > stop:
                # Insert before this entry, with specified or next color.
                self._gradient.insert(n, (stop, color or g[1]))
                break
        self._constrain_gradient()
        self.gradientChanged.emit()
        self.update()

    def removeStopAtPosition(self, n):
        if n not in self._end_stops:
            del self._gradient[n]
            self.gradientChanged.emit()
            self.update()

    def setColorAtPosition(self, n, color):
        if n < len(self._gradient):
            stop, _ = self._gradient[n]
            self._gradient[n] = stop, color
            self.gradientChanged.emit()
            self.update()

    def chooseColorAtPosition(self, n, current_color=None):
        dlg = QColorDialog(self)
        if current_color:
            dlg.setCurrentColor(QColor(current_color))

        if dlg.exec_():
            self.setColorAtPosition(n, dlg.currentColor().name())

    def _find_stop_handle_for_event(self, e, to_exclude=None):
        width = self.width()
        height = self.height()
        midpoint = height / 2

        # Are we inside a stop point? First check y.
        if e.y() >= midpoint - self._handle_h and e.y() <= midpoint + self._handle_h:
            for n, (stop, color) in enumerate(self._gradient):
                if to_exclude and n in to_exclude:
                    # Allow us to skip the extreme ends of the gradient.
                    continue
                if (
                    e.x() >= stop * width - self._handle_w
                    and e.x() <= stop * width + self._handle_w
                ):
                    return n

    def mousePressEvent(self, e):
        # We're in this stop point.
        if e.button() == Qt.MouseButton.RightButton:
            n = self._find_stop_handle_for_event(e)
            if n is not None:
                _, color = self._gradient[n]
                self.chooseColorAtPosition(n, color)

        elif e.button() == Qt.MouseButton.LeftButton:
            n = self._find_stop_handle_for_event(e, to_exclude=self._end_stops)
            if n is not None:
                # Activate drag mode.
                self._drag_position = n

    def mouseReleaseEvent(self, e):
        self._drag_position = None
        self._sort_gradient()

    def mouseMoveEvent(self, e):
        # If drag active, move the stop.
        if self._drag_position:
            stop = e.x() / self.width()
            _, color = self._gradient[self._drag_position]
            self._gradient[self._drag_position] = stop, color
            self._constrain_gradient()
            self.update()

    def mouseDoubleClickEvent(self, e):
        # Calculate the position of the click relative 0..1 to the width.
        n = self._find_stop_handle_for_event(e)
        if n:
            self._sort_gradient()  # Ensure ordered.
            # Delete existing, if not at the ends.
            if n > 0 and n < len(self._gradient) - 1:
                self.removeStopAtPosition(n)

        else:
            stop = e.x() / self.width()
            self.addStop(stop)
