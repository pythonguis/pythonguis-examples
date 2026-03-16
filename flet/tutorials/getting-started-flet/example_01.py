# Getting Started With Flet for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-flet/

import flet as ft


def main(page: ft.Page):
    page.title = "Flet First App"
    page.window.width = 200
    page.window.height = 100
    page.add(ft.Text("Hello, World!"))


ft.app(target=main)
