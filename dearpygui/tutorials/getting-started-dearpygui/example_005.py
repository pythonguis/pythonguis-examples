# Getting Started With DearPyGui for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-dearpygui/

import numpy as np

import dearpygui.dearpygui as dpg


def main() -> None:
    dpg.create_context()
    dpg.create_viewport(title="Plotting Example", width=420, height=320)

    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    with dpg.window(label="Plot Window", width=400, height=280, pos=(10, 10)):
        with dpg.plot(label="Sine and Cosine Plot", height=200, width=360):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="X")
            with dpg.plot_axis(dpg.mvYAxis, label="Y"):
                dpg.add_line_series(x.tolist(), y1.tolist(), label="sin(x)")
                dpg.add_line_series(x.tolist(), y2.tolist(), label="cos(x)")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
