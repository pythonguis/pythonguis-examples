# Getting Started With Flet for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-flet/

import flet as ft


def main(page: ft.Page):
    page.title = "Flet Dialog Demo"
    page.window.width = 300
    page.window.height = 300

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation"),
        content=ft.Text("Do you want to exit?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: on_dlg_button_click(e)),
            ft.TextButton("No", on_click=lambda e: on_dlg_button_click(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_dlg_button_click(e):
        if e.control.text == "Yes":
            page.window.close()
        page.close(dlg_modal)

    page.add(
        ft.ElevatedButton(
            "Exit",
            on_click=lambda e: page.open(dlg_modal),
        ),
    )


ft.app(target=main)
