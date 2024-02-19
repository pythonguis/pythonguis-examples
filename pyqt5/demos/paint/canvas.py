import random

import constants
from PyQt5.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt5.QtGui import (
    QBitmap,
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPen,
    QPixmap,
    QPolygon,
)
from PyQt5.QtWidgets import QLabel
from utils import build_font


class Canvas(QLabel):
    mode = "rectangle"

    primary_color = QColor(Qt.GlobalColor.black)
    secondary_color = None

    primary_color_updated = pyqtSignal(str)
    secondary_color_updated = pyqtSignal(str)

    # Store configuration settings, including pen width, fonts etc.
    config = {
        # Drawing options.
        "size": 1,
        "fill": True,
        # Font options.
        "font": QFont("Times"),
        "fontsize": 12,
        "bold": False,
        "italic": False,
        "underline": False,
    }

    active_color = None
    preview_pen = None

    timer_event = None

    current_stamp = None

    def initialize(self):
        self.background_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.GlobalColor.white)
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.GlobalColor.white)
        self.eraser_color.setAlpha(100)
        self.reset()

    def reset(self):
        # Create the pixmap for display.
        self.setPixmap(QPixmap(*constants.CANVAS_DIMENSIONS))

        # Clear the canvas.
        self.pixmap().fill(self.background_color)

    def set_primary_color(self, hex):
        self.primary_color = QColor(hex)

    def set_secondary_color(self, hex):
        self.secondary_color = QColor(hex)

    def set_config(self, key, value):
        self.config[key] = value

    def set_mode(self, mode):
        # Clean up active timer animations.
        self.timer_cleanup()
        # Reset mode-specific vars (all)
        self.active_shape_fn = None
        self.active_shape_args = ()

        self.origin_pos = None

        self.current_pos = None
        self.last_pos = None

        self.history_pos = None
        self.last_history = []

        self.current_text = ""
        self.last_text = ""

        self.last_config = {}

        self.dash_offset = 0
        self.locked = False
        # Apply the mode
        self.mode = mode

    def reset_mode(self):
        self.set_mode(self.mode)

    def on_timer(self):
        if self.timer_event:
            self.timer_event()

    def timer_cleanup(self):
        if self.timer_event:
            # Stop the timer, then trigger cleanup.
            timer_event = self.timer_event
            self.timer_event = None
            timer_event(final=True)

    # Mouse events.

    def mousePressEvent(self, e):
        fn = getattr(self, "%s_mousePressEvent" % self.mode, None)
        if fn:
            return fn(e)

    def mouseMoveEvent(self, e):
        fn = getattr(self, "%s_mouseMoveEvent" % self.mode, None)
        if fn:
            return fn(e)

    def mouseReleaseEvent(self, e):
        fn = getattr(self, "%s_mouseReleaseEvent" % self.mode, None)
        if fn:
            return fn(e)

    def mouseDoubleClickEvent(self, e):
        fn = getattr(self, "%s_mouseDoubleClickEvent" % self.mode, None)
        if fn:
            return fn(e)

    # Generic events (shared by brush-like tools)

    def generic_mousePressEvent(self, e):
        self.last_pos = e.pos()

        if e.button() == Qt.MouseButton.LeftButton:
            self.active_color = self.primary_color
        else:
            self.active_color = self.secondary_color

    def generic_mouseReleaseEvent(self, e):
        self.last_pos = None

    # Mode-specific events.

    # Select polygon events

    def selectpoly_mousePressEvent(self, e):
        if not self.locked or e.button == Qt.MouseButton.RightButton:
            self.active_shape_fn = "drawPolygon"
            self.preview_pen = constants.SELECTION_PEN
            self.generic_poly_mousePressEvent(e)

    def selectpoly_timerEvent(self, final=False):
        self.generic_poly_timerEvent(final)

    def selectpoly_mouseMoveEvent(self, e):
        if not self.locked:
            self.generic_poly_mouseMoveEvent(e)

    def selectpoly_mouseDoubleClickEvent(self, e):
        self.current_pos = e.pos()
        self.locked = True

    def selectpoly_copy(self):
        """
        Copy a polygon region from the current image, returning it.

        Create a mask for the selected area, and use it to blank
        out non-selected regions. Then get the bounding rect of the
        selection and crop to produce the smallest possible image.

        :return: QPixmap of the copied region.
        """
        self.timer_cleanup()

        pixmap = self.pixmap().copy()
        bitmap = QBitmap(*constants.CANVAS_DIMENSIONS)
        bitmap.clear()  # Starts with random data visible.

        p = QPainter(bitmap)
        # Construct a mask where the user selected area will be kept,
        # the rest removed from the image is transparent.
        userpoly = QPolygon(self.history_pos + [self.current_pos])
        p.setPen(QPen(Qt.GlobalColor.color1))
        p.setBrush(QBrush(Qt.GlobalColor.color1))  # Solid color, Qt.color1 == bit on.
        p.drawPolygon(userpoly)
        p.end()

        # Set our created mask on the image.
        pixmap.setMask(bitmap)

        # Calculate the bounding rect and return a copy of that region.
        return pixmap.copy(userpoly.boundingRect())

    # Select rectangle events

    def selectrect_mousePressEvent(self, e):
        self.active_shape_fn = "drawRect"
        self.preview_pen = constants.SELECTION_PEN
        self.generic_shape_mousePressEvent(e)

    def selectrect_timerEvent(self, final=False):
        self.generic_shape_timerEvent(final)

    def selectrect_mouseMoveEvent(self, e):
        if not self.locked:
            self.current_pos = e.pos()

    def selectrect_mouseReleaseEvent(self, e):
        self.current_pos = e.pos()
        self.locked = True

    def selectrect_copy(self):
        """
        Copy a rectangle region of the current image, returning it.

        :return: QPixmap of the copied region.
        """
        self.timer_cleanup()
        return self.pixmap().copy(QRect(self.origin_pos, self.current_pos))

    # Eraser events

    def eraser_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def eraser_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(
                QPen(
                    self.eraser_color,
                    30,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def eraser_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    # Stamp (pie) events

    def stamp_mousePressEvent(self, e):
        p = QPainter(self.pixmap())
        stamp = self.current_stamp
        p.drawPixmap(
            e.x() - stamp.width() // 2,
            e.y() - stamp.height() // 2,
            stamp,
        )
        self.update()

    # Pen events

    def pen_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def pen_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(
                QPen(
                    self.active_color,
                    self.config["size"],
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def pen_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    # Brush events

    def brush_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def brush_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(
                QPen(
                    self.active_color,
                    self.config["size"] * constants.BRUSH_MULT,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def brush_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    # Spray events

    def spray_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def spray_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.active_color, 1))

            for n in range(self.config["size"] * constants.SPRAY_PAINT_N):
                xo = random.gauss(0, self.config["size"] * constants.SPRAY_PAINT_MULT)
                yo = random.gauss(0, self.config["size"] * constants.SPRAY_PAINT_MULT)
                p.drawPoint(e.x() + xo, e.y() + yo)

        self.update()

    def spray_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    # Text events

    def keyPressEvent(self, e):
        if self.mode == "text":
            if e.key() == Qt.Key.Key_Backspace:
                self.current_text = self.current_text[:-1]
            else:
                self.current_text = self.current_text + e.text()

    def text_mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self.current_pos is None:
            self.current_pos = e.pos()
            self.current_text = ""
            self.timer_event = self.text_timerEvent

        elif e.button() == Qt.MouseButton.LeftButton:
            self.timer_cleanup()
            # Draw the text to the image
            p = QPainter(self.pixmap())
            p.setRenderHints(QPainter.RenderHint.Antialiasing)
            font = build_font(self.config)
            p.setFont(font)
            pen = QPen(
                self.primary_color,
                1,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
            p.setPen(pen)
            p.drawText(self.current_pos, self.current_text)
            self.update()

            self.reset_mode()

        elif e.button() == Qt.MouseButton.RightButton and self.current_pos:
            self.reset_mode()

    def text_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
        pen = constants.PREVIEW_PEN
        p.setPen(pen)
        if self.last_text:
            font = build_font(self.last_config)
            p.setFont(font)
            p.drawText(self.current_pos, self.last_text)

        if not final:
            font = build_font(self.config)
            p.setFont(font)
            p.drawText(self.current_pos, self.current_text)

        self.last_text = self.current_text
        self.last_config = self.config.copy()
        self.update()

    # Fill events

    def fill_mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.active_color = self.primary_color
        else:
            self.active_color = self.secondary_color

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
        p = QPainter(self.pixmap())
        p.setPen(QPen(self.active_color))

        while queue:
            x, y = queue.pop()
            if image.pixel(x, y) == target_color:
                p.drawPoint(QPoint(x, y))
                queue.extend(get_cardinal_points(have_seen, (x, y)))

        self.update()

    # Dropper events

    def dropper_mousePressEvent(self, e):
        c = self.pixmap().toImage().pixel(e.pos())
        hex = QColor(c).name()

        if e.button() == Qt.MouseButton.LeftButton:
            self.set_primary_color(hex)
            self.primary_color_updated.emit(hex)  # Update UI.

        elif e.button() == Qt.MouseButton.RightButton:
            self.set_secondary_color(hex)
            self.secondary_color_updated.emit(hex)  # Update UI.

    # Generic shape events: Rectangle, Ellipse, Rounded-rect

    def generic_shape_mousePressEvent(self, e):
        self.origin_pos = e.pos()
        self.current_pos = e.pos()
        self.timer_event = self.generic_shape_timerEvent

    def generic_shape_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
        pen = self.preview_pen
        pen.setDashOffset(self.dash_offset)
        p.setPen(pen)
        if self.last_pos:
            getattr(p, self.active_shape_fn)(QRect(self.origin_pos, self.last_pos), *self.active_shape_args)

        if not final:
            self.dash_offset -= 1
            pen.setDashOffset(self.dash_offset)
            p.setPen(pen)
            getattr(p, self.active_shape_fn)(QRect(self.origin_pos, self.current_pos), *self.active_shape_args)

        self.update()
        self.last_pos = self.current_pos

    def generic_shape_mouseMoveEvent(self, e):
        self.current_pos = e.pos()

    def generic_shape_mouseReleaseEvent(self, e):
        if self.last_pos:
            # Clear up indicator.
            self.timer_cleanup()

            p = QPainter(self.pixmap())
            p.setPen(
                QPen(
                    self.primary_color,
                    self.config["size"],
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )

            if self.config["fill"]:
                p.setBrush(QBrush(self.secondary_color))
            getattr(p, self.active_shape_fn)(QRect(self.origin_pos, e.pos()), *self.active_shape_args)
            self.update()

        self.reset_mode()

    # Line events

    def line_mousePressEvent(self, e):
        self.origin_pos = e.pos()
        self.current_pos = e.pos()
        self.preview_pen = constants.PREVIEW_PEN
        self.timer_event = self.line_timerEvent

    def line_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
        pen = self.preview_pen
        p.setPen(pen)
        if self.last_pos:
            p.drawLine(self.origin_pos, self.last_pos)

        if not final:
            p.drawLine(self.origin_pos, self.current_pos)

        self.update()
        self.last_pos = self.current_pos

    def line_mouseMoveEvent(self, e):
        self.current_pos = e.pos()

    def line_mouseReleaseEvent(self, e):
        if self.last_pos:
            # Clear up indicator.
            self.timer_cleanup()

            p = QPainter(self.pixmap())
            p.setPen(
                QPen(
                    self.primary_color,
                    self.config["size"],
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )

            p.drawLine(self.origin_pos, e.pos())
            self.update()

        self.reset_mode()

    # Generic poly events
    def generic_poly_mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            if self.history_pos:
                self.history_pos.append(e.pos())
            else:
                self.history_pos = [e.pos()]
                self.current_pos = e.pos()
                self.timer_event = self.generic_poly_timerEvent

        elif e.button() == Qt.MouseButton.RightButton and self.history_pos:
            # Clean up, we're not drawing
            self.timer_cleanup()
            self.reset_mode()

    def generic_poly_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.CompositionMode.RasterOp_SourceXorDestination)
        pen = self.preview_pen
        pen.setDashOffset(self.dash_offset)
        p.setPen(pen)
        if self.last_history:
            getattr(p, self.active_shape_fn)(*self.last_history)

        if not final:
            self.dash_offset -= 1
            pen.setDashOffset(self.dash_offset)
            p.setPen(pen)
            getattr(p, self.active_shape_fn)(*self.history_pos + [self.current_pos])

        self.update()
        self.last_pos = self.current_pos
        self.last_history = self.history_pos + [self.current_pos]

    def generic_poly_mouseMoveEvent(self, e):
        self.current_pos = e.pos()

    def generic_poly_mouseDoubleClickEvent(self, e):
        self.timer_cleanup()
        p = QPainter(self.pixmap())
        p.setPen(
            QPen(
                self.primary_color,
                self.config["size"],
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )

        # Note the brush is ignored for polylines.
        if self.secondary_color:
            p.setBrush(QBrush(self.secondary_color))

        getattr(p, self.active_shape_fn)(*self.history_pos + [e.pos()])
        self.update()
        self.reset_mode()

    # Polyline events

    def polyline_mousePressEvent(self, e):
        self.active_shape_fn = "drawPolyline"
        self.preview_pen = constants.PREVIEW_PEN
        self.generic_poly_mousePressEvent(e)

    def polyline_timerEvent(self, final=False):
        self.generic_poly_timerEvent(final)

    def polyline_mouseMoveEvent(self, e):
        self.generic_poly_mouseMoveEvent(e)

    def polyline_mouseDoubleClickEvent(self, e):
        self.generic_poly_mouseDoubleClickEvent(e)

    # Rectangle events

    def rect_mousePressEvent(self, e):
        self.active_shape_fn = "drawRect"
        self.active_shape_args = ()
        self.preview_pen = constants.PREVIEW_PEN
        self.generic_shape_mousePressEvent(e)

    def rect_timerEvent(self, final=False):
        self.generic_shape_timerEvent(final)

    def rect_mouseMoveEvent(self, e):
        self.generic_shape_mouseMoveEvent(e)

    def rect_mouseReleaseEvent(self, e):
        self.generic_shape_mouseReleaseEvent(e)

    # Polygon events

    def polygon_mousePressEvent(self, e):
        self.active_shape_fn = "drawPolygon"
        self.preview_pen = constants.PREVIEW_PEN
        self.generic_poly_mousePressEvent(e)

    def polygon_timerEvent(self, final=False):
        self.generic_poly_timerEvent(final)

    def polygon_mouseMoveEvent(self, e):
        self.generic_poly_mouseMoveEvent(e)

    def polygon_mouseDoubleClickEvent(self, e):
        self.generic_poly_mouseDoubleClickEvent(e)

    # Ellipse events

    def ellipse_mousePressEvent(self, e):
        self.active_shape_fn = "drawEllipse"
        self.active_shape_args = ()
        self.preview_pen = constants.PREVIEW_PEN
        self.generic_shape_mousePressEvent(e)

    def ellipse_timerEvent(self, final=False):
        self.generic_shape_timerEvent(final)

    def ellipse_mouseMoveEvent(self, e):
        self.generic_shape_mouseMoveEvent(e)

    def ellipse_mouseReleaseEvent(self, e):
        self.generic_shape_mouseReleaseEvent(e)

    # Roundedrect events

    def roundrect_mousePressEvent(self, e):
        self.active_shape_fn = "drawRoundedRect"
        self.active_shape_args = (25, 25)
        self.preview_pen = constants.PREVIEW_PEN
        self.generic_shape_mousePressEvent(e)

    def roundrect_timerEvent(self, final=False):
        self.generic_shape_timerEvent(final)

    def roundrect_mouseMoveEvent(self, e):
        self.generic_shape_mouseMoveEvent(e)

    def roundrect_mouseReleaseEvent(self, e):
        self.generic_shape_mouseReleaseEvent(e)
