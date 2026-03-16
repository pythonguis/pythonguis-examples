# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from nicegui import ui


def on_button_click():
    ui.notify("Button was clicked!")


def on_checkbox_change(event):
    state = "checked" if event.value else "unchecked"
    ui.notify(f"Checkbox is {state}")


def on_slider_change(event):
    ui.notify(f"Slider value: {event.value}")


def on_input_change(event):
    ui.notify(f"Input changed to: {event.value}")


ui.label("Event Handling Demo")

ui.button("Click Me", on_click=on_button_click)

ui.checkbox("Check Me", on_change=on_checkbox_change)

ui.slider(min=0, max=10, value=5, on_change=on_slider_change)

ui.input("Type something", on_change=on_input_change)

ui.run(title="NiceGUI Events & Actions Demo")
