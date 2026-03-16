# Getting Started With DearPyGui for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-dearpygui/

import dearpygui.dearpygui as dpg


def main():
    dpg.create_context()
    dpg.create_viewport(title="Viewport", width=300, height=100)

    with dpg.window(label="DearPyGui Demo", width=300, height=100):
        dpg.add_text("Hello, World!")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
