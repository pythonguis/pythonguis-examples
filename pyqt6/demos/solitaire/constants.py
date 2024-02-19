import os

from PyQt6.QtCore import QRect, QSize
from PyQt6.QtGui import QImage

WINDOW_SIZE = 840, 600

CARD_DIMENSIONS = QSize(80, 116)
CARD_RECT = QRect(0, 0, 80, 116)
CARD_SPACING_X = 110
CARD_BACK = QImage(os.path.join("images", "back.png"))

DEAL_RECT = QRect(30, 30, 110, 140)

OFFSET_X = 50
OFFSET_Y = 50
WORK_STACK_Y = 200

SIDE_FACE = 0
SIDE_BACK = 1

BOUNCE_ENERGY = 0.8

# We store cards as numbers 1-13, since we only need
# to know their order for solitaire.
SUITS = ["C", "S", "H", "D"]
