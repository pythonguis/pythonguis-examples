# Getting Started With Flet for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-flet/

import flet as ft


def main(page: ft.Page):
    page.title = "Flet Buttons Demo"
    page.window.width = 200
    page.window.height = 200

    page.add(ft.ElevatedButton("Elevated Button"))
    page.add(ft.FilledButton("Filled Button"))
    page.add(ft.FloatingActionButton(icon=ft.Icons.ADD))


ft.app(target=main)
