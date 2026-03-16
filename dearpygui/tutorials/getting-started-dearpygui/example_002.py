# Getting Started With DearPyGui for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-dearpygui/

import dearpygui.dearpygui as dpg


def main():
    dpg.create_context()
    dpg.create_viewport(title="Widgets Demo", width=400, height=640)

    with dpg.window(
        label="Basic DearPyGui Widgets",
        width=380,
        height=610,
        pos=(10, 10),
    ):
        dpg.add_text("Static label")
        dpg.add_input_text(
            label="Text Input",
            default_value="Type some text here...",
            tag="widget_input",
        )
        dpg.add_button(label="Click Me!")
        dpg.add_checkbox(label="Check Me!")
        dpg.add_radio_button(
            ("DearPyGui", "PyQt6", "PySide6"),
        )

        dpg.add_slider_int(
            label="Int Slider",
            default_value=5,
            min_value=0,
            max_value=10,
        )
        dpg.add_slider_float(
            label="Float Slider",
            default_value=0.5,
            min_value=0.0,
            max_value=1.0,
        )

        dpg.add_combo(
            ("DearPyGui", "PyQt6", "PySide6"),
            label="GUI Library",
        )
        dpg.add_color_picker(label="Pick a Color")
        dpg.add_progress_bar(
            label="Progress",
            default_value=0.5,
            width=250,
        )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
