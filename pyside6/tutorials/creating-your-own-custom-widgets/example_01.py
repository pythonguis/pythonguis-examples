from power_bar import PowerBar

from PySide6 import QtWidgets

app = QtWidgets.QApplication([])
bar = PowerBar(
    [
        "#49006a",
        "#7a0177",
        "#ae017e",
        "#dd3497",
        "#f768a1",
        "#fa9fb5",
        "#fcc5c0",
        "#fde0dd",
        "#fff7f3",
    ]
)
bar.setBarPadding(2)
bar.setBarSolidPercent(0.9)
bar.setBackgroundColor("gray")
bar.show()
app.exec()
