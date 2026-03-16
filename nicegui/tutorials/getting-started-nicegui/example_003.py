# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from nicegui import ui

# Control elements
ui.button("Button")

with ui.dropdown_button("Edit", icon="edit", auto_close=True):
    ui.item("Copy")
    ui.item("Paste")
    ui.item("Cut")

ui.toggle(["ON", "OFF"], value="ON")

ui.radio(["NiceGUI", "PyQt6", "PySide6"], value="NiceGUI").props("inline")

ui.checkbox("Enable Feature")

ui.slider(min=0, max=100, value=50, step=5)

ui.switch("Dark Mode")

ui.input("Your Name")

ui.number("Age", min=0, max=120, value=25, step=1)

ui.select(
    ["NiceGUI", "PyQt6", "PySide6"],
    value="NiceGUI",
)

ui.date(value="2025-04-11")

ui.run(title="NiceGUI Control Elements")
