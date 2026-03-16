# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from nicegui import ui

with ui.image("./otje.jpg"):
    ui.label("Otje the cat!").classes("absolute-bottom text-subtitle2 text-center")


ui.run(title="NiceGUI Audiovisual Elements")
