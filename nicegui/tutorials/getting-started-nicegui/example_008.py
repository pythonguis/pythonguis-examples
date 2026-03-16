# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from nicegui import ui


def on_click(event):
    ui.notify("Button was clicked!")


def on_hover(event):
    ui.notify("Button was hovered!")


button = ui.button("Button")
button.on("click", on_click)
button.on("mouseover", on_hover)

ui.run()
