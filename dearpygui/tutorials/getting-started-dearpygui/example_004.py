# Getting Started With DearPyGui for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-dearpygui/

import dearpygui.dearpygui as dpg


def on_click_callback(sender, app_data, user_data):
    text = dpg.get_value("input_text")
    dpg.set_value("dialog_text", f'You typed: "{text}"')
    dpg.configure_item("dialog", show=True)


def main() -> None:
    dpg.create_context()
    dpg.create_viewport(title="Callback Example", width=270, height=120)

    with dpg.window(label="Callback Example", width=250, height=80, pos=(10, 10)):
        dpg.add_text("Type something and press Click Me!")
        dpg.add_input_text(label="Input", tag="input_text")
        dpg.add_button(label="Click Me!", callback=on_click_callback)
        with dpg.window(
            label="Dialog",
            modal=True,
            show=False,
            width=230,
            height=80,
            tag="dialog",
            no_close=True,
            pos=(10, 10),
        ):
            dpg.add_text("", tag="dialog_text")
            dpg.add_button(
                label="OK",
                callback=lambda s, a, u: dpg.configure_item("dialog", show=False),
            )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
