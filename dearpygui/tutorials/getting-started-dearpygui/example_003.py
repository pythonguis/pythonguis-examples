# Getting Started With DearPyGui for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-dearpygui/

import dearpygui.dearpygui as dpg


def main():
    dpg.create_context()
    dpg.create_viewport(title="Layout Demo", width=520, height=420)

    with dpg.window(
        label="Layout Demo",
        width=500,
        height=380,
        pos=(10, 10),
    ):
        dpg.add_text("1) Vertical layout:")
        dpg.add_button(label="Top")
        dpg.add_button(label="Middle")
        dpg.add_button(label="Bottom")

        dpg.add_spacer(height=12)

        dpg.add_text("2) Horizontal layout:")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Left")
            dpg.add_button(label="Center")
            dpg.add_button(label="Right")

        dpg.add_spacer(height=12)

        dpg.add_text("3) Indentation:")
        dpg.add_checkbox(label="Indented at creation (30px)", indent=30)
        dpg.add_checkbox(label="Indented after creation (35px)", tag="indent_b")
        dpg.configure_item("indent_b", indent=35)

        dpg.add_spacer(height=12)

        dpg.add_text("4) Absolute positioning:")
        dpg.add_text("Positioned at creation: (x=100, y=300)", pos=(100, 300))
        dpg.add_text("Positioned after creation: (x=100, y=320)", tag="move_me")
        dpg.set_item_pos("move_me", [100, 320])

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
