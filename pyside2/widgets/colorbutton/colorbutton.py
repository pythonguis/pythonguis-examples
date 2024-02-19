from PySide2.QtCore import Qt
from PySide2.QtCore import Signal as Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QColorDialog, QPushButton


class ColorButton(QPushButton):
    """
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to the default color (None by default).
    """

    colorChanged = Signal(object)

    def __init__(self, *args, color=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)
        self.setObjectName("ColorButton")
        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)

        # Set the initial/default state.
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            self.setStyleSheet(f"#ColorButton {{background-color: {self._color};}}")
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        """
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        """
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.setColor(self._default)

        return super().mousePressEvent(e)
