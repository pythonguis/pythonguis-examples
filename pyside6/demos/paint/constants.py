from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen

BRUSH_MULT = 3
SPRAY_PAINT_MULT = 5
SPRAY_PAINT_N = 100

COLORS = [
    "#000000",
    "#82817f",
    "#820300",
    "#868417",
    "#007e03",
    "#037e7b",
    "#040079",
    "#81067a",
    "#7f7e45",
    "#05403c",
    "#0a7cf6",
    "#093c7e",
    "#7e07f9",
    "#7c4002",
    "#ffffff",
    "#c1c1c1",
    "#f70406",
    "#fffd00",
    "#08fb01",
    "#0bf8ee",
    "#0000fa",
    "#b92fc2",
    "#fffc91",
    "#00fd83",
    "#87f9f9",
    "#8481c4",
    "#dc137d",
    "#fb803c",
]

FONT_SIZES = [
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    18,
    24,
    36,
    48,
    64,
    72,
    96,
    144,
    288,
]

MODES = [
    "selectpoly",
    "selectrect",
    "eraser",
    "fill",
    "dropper",
    "stamp",
    "pen",
    "brush",
    "spray",
    "text",
    "line",
    "polyline",
    "rect",
    "polygon",
    "ellipse",
    "roundrect",
]

CANVAS_DIMENSIONS = 600, 400

STAMPS = [
    ":/stamps/pie-apple.png",
    ":/stamps/pie-cherry.png",
    ":/stamps/pie-cherry2.png",
    ":/stamps/pie-lemon.png",
    ":/stamps/pie-moon.png",
    ":/stamps/pie-pork.png",
    ":/stamps/pie-pumpkin.png",
    ":/stamps/pie-walnut.png",
]

SELECTION_PEN = QPen(QColor(0xFF, 0xFF, 0xFF), 1, Qt.PenStyle.DashLine)
PREVIEW_PEN = QPen(QColor(0xFF, 0xFF, 0xFF), 1, Qt.PenStyle.SolidLine)
