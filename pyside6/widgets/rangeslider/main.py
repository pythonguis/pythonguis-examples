import sys

from PySide6.QtWidgets import QApplication
from range_slider import RangeSlider

app = QApplication(sys.argv)

slider = RangeSlider()
slider.valueChanged.connect(print)
slider.show()

app.exec()
