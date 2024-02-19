from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PySide2.QtWidgets import QLabel


class PaintWidget(QLabel):
    def __init__(self, width, height, background="white", *args, **kwargs):
        super().__init__(*args, **kwargs)
        pixmap = QPixmap(width, height)
        self.setPixmap(pixmap)

        # Fill the canvas with the initial color.
        painter = QPainter(self.pixmap())
        brush = QBrush()
        brush.setColor(QColor(background))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.fillRect(0, 0, pixmap.width(), pixmap.height(), brush)
        painter.end()

        self.last_x, self.last_y = None, None
        self._pen_color = QColor("#000000")
        self._pen_width = 4

    def setPenColor(self, c):
        self._pen_color = QColor(c)

    def setPenWidth(self, w):
        self._pen_width = int(w)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  #  Ignore the first time.

        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self._pen_width)
        p.setColor(self._pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self._flood_fill_from_event(e)

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def _flood_fill_from_event(self, e):
        image = self.pixmap().toImage()
        w, h = image.width(), image.height()
        x, y = e.x(), e.y()

        # Get our target color from origin.
        target_color = image.pixel(x, y)

        have_seen = set()
        queue = [(x, y)]

        def get_cardinal_points(have_seen, center_pos):
            points = []
            cx, cy = center_pos
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x, cy + y
                if xx >= 0 and xx < w and yy >= 0 and yy < h and (xx, yy) not in have_seen:
                    points.append((xx, yy))
                    have_seen.add((xx, yy))

            return points

        # Now perform the search and fill.
        painter = QPainter(self.pixmap())
        painter.setPen(QPen(self._pen_color))

        while queue:
            x, y = queue.pop()
            if image.pixel(x, y) == target_color:
                painter.drawPoint(QPoint(x, y))
                queue.extend(get_cardinal_points(have_seen, (x, y)))

        self.update()
