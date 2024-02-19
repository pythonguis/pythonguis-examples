import random
import sys
import types

import constants
import resources_rc
from canvas import Canvas
from MainWindow import Ui_MainWindow
from PySide6.QtCore import QPoint, QRect, Qt, QTimer
from PySide6.QtGui import (
    QFont,
    QIcon,
    QImage,
    QPixmap,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QColorDialog,
    QComboBox,
    QFileDialog,
    QFontComboBox,
    QLabel,
    QMainWindow,
    QSlider,
)

# Not actually required, the import triggers this already.
resources_rc.qInitResources()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Replace canvas placeholder from QtDesigner.
        self.horizontalLayout.removeWidget(self.canvas)
        self.canvas = Canvas()
        self.canvas.initialize()
        # We need to enable mouse tracking to follow the mouse without the button pressed.
        self.canvas.setMouseTracking(True)
        # Enable focus to capture key inputs.
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.horizontalLayout.addWidget(self.canvas)

        # Setup the mode buttons
        mode_group = QButtonGroup(self)
        mode_group.setExclusive(True)

        for mode in constants.MODES:
            btn = getattr(self, "%sButton" % mode)
            btn.pressed.connect(lambda mode=mode: self.canvas.set_mode(mode))
            mode_group.addButton(btn)

        # Setup the color selection buttons.
        self.primaryButton.pressed.connect(
            lambda: self.choose_color(self.set_primary_color)
        )
        self.secondaryButton.pressed.connect(
            lambda: self.choose_color(self.set_secondary_color)
        )

        # Initialize button colours.
        for n, hex in enumerate(constants.COLORS, 1):
            btn = getattr(self, "colorButton_%d" % n)
            btn.setStyleSheet("QPushButton { background-color: %s; }" % hex)
            btn.hex = hex  # For use in the event below

            def patch_mousePressEvent(self_, e):
                if e.button() == Qt.MouseButton.LeftButton:
                    self.set_primary_color(self_.hex)

                elif e.button() == Qt.MouseButton.RightButton:
                    self.set_secondary_color(self_.hex)

            btn.mousePressEvent = types.MethodType(patch_mousePressEvent, btn)

        # Setup up action signals
        self.actionCopy.triggered.connect(self.copy_to_clipboard)

        # Initialize animation timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.canvas.on_timer)
        self.timer.setInterval(100)
        self.timer.start()

        # Setup to agree with Canvas.
        self.set_primary_color("#000000")
        self.set_secondary_color("#ffffff")

        # Signals for canvas-initiated color changes (dropper).
        self.canvas.primary_color_updated.connect(self.set_primary_color)
        self.canvas.secondary_color_updated.connect(self.set_secondary_color)

        # Setup the stamp state.
        self.current_stamp_n = -1
        self.next_stamp()
        self.stampnextButton.pressed.connect(self.next_stamp)

        # Menu options
        self.actionNewImage.triggered.connect(self.canvas.initialize)
        self.actionOpenImage.triggered.connect(self.open_file)
        self.actionSaveImage.triggered.connect(self.save_file)
        self.actionClearImage.triggered.connect(self.canvas.reset)
        self.actionInvertColors.triggered.connect(self.invert)
        self.actionFlipHorizontal.triggered.connect(self.flip_horizontal)
        self.actionFlipVertical.triggered.connect(self.flip_vertical)

        # Setup the drawing toolbar.
        self.fontselect = QFontComboBox()
        self.fontToolbar.addWidget(self.fontselect)
        self.fontselect.currentFontChanged.connect(
            lambda f: self.canvas.set_config("font", f)
        )
        self.fontselect.setCurrentFont(QFont("Times"))

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in constants.FONT_SIZES])
        self.fontsize.currentTextChanged.connect(
            lambda f: self.canvas.set_config("fontsize", int(f))
        )

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontToolbar.addWidget(self.fontsize)

        self.fontToolbar.addAction(self.actionBold)
        self.actionBold.triggered.connect(lambda s: self.canvas.set_config("bold", s))
        self.fontToolbar.addAction(self.actionItalic)
        self.actionItalic.triggered.connect(
            lambda s: self.canvas.set_config("italic", s)
        )
        self.fontToolbar.addAction(self.actionUnderline)
        self.actionUnderline.triggered.connect(
            lambda s: self.canvas.set_config("underline", s)
        )

        sizeicon = QLabel()
        sizeicon.setPixmap(QPixmap(":/icons/border-weight.png"))
        self.drawingToolbar.addWidget(sizeicon)
        self.sizeselect = QSlider()
        self.sizeselect.setRange(1, 20)
        self.sizeselect.setOrientation(Qt.Orientation.Horizontal)
        self.sizeselect.valueChanged.connect(
            lambda s: self.canvas.set_config("size", s)
        )
        self.drawingToolbar.addWidget(self.sizeselect)

        self.actionFillShapes.triggered.connect(
            lambda s: self.canvas.set_config("fill", s)
        )
        self.drawingToolbar.addAction(self.actionFillShapes)
        self.actionFillShapes.setChecked(True)

        self.show()

    def choose_color(self, callback):
        dlg = QColorDialog()
        if dlg.exec():
            callback(dlg.selectedColor().name())

    def set_primary_color(self, hex):
        self.canvas.set_primary_color(hex)
        self.primaryButton.setStyleSheet("QPushButton { background-color: %s; }" % hex)

    def set_secondary_color(self, hex):
        self.canvas.set_secondary_color(hex)
        self.secondaryButton.setStyleSheet(
            "QPushButton { background-color: %s; }" % hex
        )

    def next_stamp(self):
        self.current_stamp_n += 1
        if self.current_stamp_n >= len(constants.STAMPS):
            self.current_stamp_n = 0

        pixmap = QPixmap(constants.STAMPS[self.current_stamp_n])
        self.stampnextButton.setIcon(QIcon(pixmap))

        self.canvas.current_stamp = pixmap

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()

        if self.canvas.mode == "selectrect" and self.canvas.locked:
            clipboard.setPixmap(self.canvas.selectrect_copy())

        elif self.canvas.mode == "selectpoly" and self.canvas.locked:
            clipboard.setPixmap(self.canvas.selectpoly_copy())

        else:
            clipboard.setPixmap(self.canvas.pixmap())

    def open_file(self):
        """
        Open image file for editing, scaling the smaller dimension and cropping the remainder.
        :return:
        """
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "PNG image files (*.png); JPEG image files (*jpg); All files (*.*)",
        )

        if path:
            pixmap = QPixmap()
            pixmap.load(path)

            # We need to crop down to the size of our canvas. Get the size of the loaded image.
            iw = pixmap.width()
            ih = pixmap.height()

            # Get the size of the space we're filling.
            cw, ch = constants.CANVAS_DIMENSIONS

            if iw / cw < ih / ch:  # The height is relatively bigger than the width.
                pixmap = pixmap.scaledToWidth(cw)
                hoff = (pixmap.height() - ch) // 2
                pixmap = pixmap.copy(
                    QRect(
                        QPoint(0, hoff),
                        QPoint(cw, pixmap.height() - hoff),
                    )
                )

            elif iw / cw > ih / ch:  # The height is relatively bigger than the width.
                pixmap = pixmap.scaledToHeight(ch)
                woff = (pixmap.width() - cw) // 2
                pixmap = pixmap.copy(
                    QRect(
                        QPoint(woff, 0),
                        QPoint(pixmap.width() - woff, ch),
                    )
                )

            self.canvas.setPixmap(pixmap)

    def save_file(self):
        """
        Save active canvas to image file.
        :return:
        """
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "PNG Image file (*.png)"
        )

        if path:
            pixmap = self.canvas.pixmap()
            pixmap.save(path, "PNG")

    def invert(self):
        img = QImage(self.canvas.pixmap())
        img.invertPixels()
        pixmap = QPixmap()
        pixmap.convertFromImage(img)
        self.canvas.setPixmap(pixmap)

    def flip_horizontal(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(-1, 1)))

    def flip_vertical(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(1, -1)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icons/piecasso.ico"))
    window = MainWindow()
    app.exec()
