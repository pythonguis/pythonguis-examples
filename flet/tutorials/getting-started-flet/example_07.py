# Getting Started With Flet for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-flet/

import flet as ft


def main(page: ft.Page):
    page.title = "Flet Layouts Demo"
    page.window.width = 250
    page.window.height = 300

    main_layout = ft.Column(
        [
            ft.Text("1) Vertical layout:"),
            ft.ElevatedButton("Top"),
            ft.ElevatedButton("Middle"),
            ft.ElevatedButton("Bottom"),
            ft.Container(height=12),  # Spacer
            ft.Text("2) Horizontal layout:"),
            ft.Row(
                [
                    ft.ElevatedButton("Left"),
                    ft.ElevatedButton("Center"),
                    ft.ElevatedButton("Right"),
                ]
            ),
        ],
    )

    page.add(main_layout)


ft.app(target=main)
