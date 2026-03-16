# Getting Started With Flet for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-flet/

import flet as ft


def main(page: ft.Page):
    page.title = "Flet Event & Callback Demo"
    page.window.width = 340
    page.window.height = 360

    def on_click(e):  # Event handler or callback function
        dialog_text.value = f'You typed: "{txt_input.value}"'
        page.open(dialog)
        page.update()

    txt_input = ft.TextField(label="Type something and press Click Me!")
    btn = ft.ElevatedButton("Click Me!", on_click=on_click)
    dialog_text = ft.Text("")
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Dialog"),
        content=dialog_text,
        actions=[ft.TextButton("OK", on_click=lambda e: page.close(dialog))],
        open=False,
    )

    page.add(
        txt_input,
        btn,
    )


ft.app(target=main)
