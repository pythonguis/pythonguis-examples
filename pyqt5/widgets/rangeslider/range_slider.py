from PyQt5.QtCore import QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QMouseEvent, QPainter, QPaintEvent, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QSizePolicy,
    QSlider,
    QStyle,
    QStyleOptionSlider,
    QWidget,
)


class RangeSlider(QWidget):
    valueChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.first_position = 1
        self.second_position = 8

        self.opt = QStyleOptionSlider()
        self.opt.minimum = 0
        self.opt.maximum = 10

        self.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.setTickInterval(1)

        self.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.ControlType.Slider,
            )
        )

    def setRangeLimit(self, minimum: int, maximum: int):
        self.opt.minimum = minimum
        self.opt.maximum = maximum

    def setRange(self, start: int, end: int):
        self.first_position = start
        self.second_position = end

    def getRange(self):
        return (self.first_position, self.second_position)

    def setTickPosition(self, position: QSlider.TickPosition):
        self.opt.tickPosition = position

    def setTickInterval(self, ti: int):
        self.opt.tickInterval = ti

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        # Draw rule
        self.opt.initFrom(self)
        self.opt.rect = self.rect()
        self.opt.sliderPosition = 0
        self.opt.subControls = (
            QStyle.SubControl.SC_SliderGroove | QStyle.SubControl.SC_SliderTickmarks
        )

        #   Draw GROOVE
        self.style().drawComplexControl(
            QStyle.ComplexControl.CC_Slider, self.opt, painter
        )

        #  Draw INTERVAL

        color = self.palette().color(QPalette.ColorRole.Highlight)
        color.setAlpha(160)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)

        self.opt.sliderPosition = self.first_position
        x_left_handle = (
            self.style()
            .subControlRect(
                QStyle.ComplexControl.CC_Slider,
                self.opt,
                QStyle.SubControl.SC_SliderHandle,
            )
            .right()
        )

        self.opt.sliderPosition = self.second_position
        x_right_handle = (
            self.style()
            .subControlRect(
                QStyle.ComplexControl.CC_Slider,
                self.opt,
                QStyle.SubControl.SC_SliderHandle,
            )
            .left()
        )

        groove_rect = self.style().subControlRect(
            QStyle.ComplexControl.CC_Slider, self.opt, QStyle.SubControl.SC_SliderGroove
        )

        selection = QRect(
            x_left_handle,
            groove_rect.y(),
            x_right_handle - x_left_handle,
            groove_rect.height(),
        ).adjusted(-1, 1, 1, -1)

        painter.drawRect(selection)

        # Draw first handle

        self.opt.subControls = QStyle.SubControl.SC_SliderHandle
        self.opt.sliderPosition = self.first_position
        self.style().drawComplexControl(
            QStyle.ComplexControl.CC_Slider, self.opt, painter
        )

        # Draw second handle
        self.opt.sliderPosition = self.second_position
        self.style().drawComplexControl(
            QStyle.ComplexControl.CC_Slider, self.opt, painter
        )

    def mousePressEvent(self, event: QMouseEvent):
        self.opt.sliderPosition = self.first_position
        self._first_sc = self.style().hitTestComplexControl(
            QStyle.ComplexControl.CC_Slider, self.opt, event.pos(), self
        )

        self.opt.sliderPosition = self.second_position
        self._second_sc = self.style().hitTestComplexControl(
            QStyle.ComplexControl.CC_Slider, self.opt, event.pos(), self
        )

    def mouseMoveEvent(self, event: QMouseEvent):
        distance = self.opt.maximum - self.opt.minimum

        pos = self.style().sliderValueFromPosition(
            0, distance, event.pos().x(), self.rect().width()
        )

        if self._first_sc == QStyle.SubControl.SC_SliderHandle:
            if pos <= self.second_position:
                self.first_position = pos
                self.valueChanged.emit(self.first_position, self.second_position)
                self.update()
                return

        if self._second_sc == QStyle.SubControl.SC_SliderHandle:
            if pos >= self.first_position:
                self.second_position = pos
                self.valueChanged.emit(self.first_position, self.second_position)
                self.update()

    def sizeHint(self):
        """override"""
        SliderLength = 84
        TickSpace = 5

        w = SliderLength
        h = self.style().pixelMetric(
            QStyle.PixelMetric.PM_SliderThickness, self.opt, self
        )

        if (
            self.opt.tickPosition & QSlider.TickPosition.TicksAbove
            or self.opt.tickPosition & QSlider.TickPosition.TicksBelow
        ):
            h += TickSpace

        return (
            self.style()
            .sizeFromContents(
                QStyle.ContentsType.CT_Slider, self.opt, QSize(w, h), self
            )
            .expandedTo(QApplication.globalStrut())
        )
