# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from nicegui import ui

with ui.card().classes("w-full max-w-3xl mx-auto shadow-lg"):
    ui.label("Profile Page").classes("text-xl font-bold")

    with ui.row().classes("w-full"):
        with ui.card():
            ui.image("./profile.png")

            with ui.card_section():
                ui.label("Profile Image").classes("text-center font-bold")
                ui.button("Change Image", icon="photo_camera")

        with ui.card().classes("flex-grow"):
            with ui.column().classes("w-full"):
                name_input = ui.input(
                    placeholder="Your Name",
                ).classes("w-full")
                gender_select = ui.select(
                    ["Male", "Female", "Other"],
                ).classes("w-full")
                eye_color_input = ui.input(
                    placeholder="Eye Color",
                ).classes("w-full")
                height_input = ui.number(
                    min=0,
                    max=250,
                    value=170,
                    step=1,
                ).classes("w-full")
                weight_input = ui.number(
                    min=0,
                    max=500,
                    value=60,
                    step=0.1,
                ).classes("w-full")

            with ui.row().classes("justify-end gap-2 q-mt-lg"):
                ui.button("Reset", icon="refresh").props("outline")
                ui.button("Save", icon="save").props("color=primary")

ui.run(title="NiceGUI Layout Elements")
