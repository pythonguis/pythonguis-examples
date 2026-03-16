# Getting Started With Flet for GUI Development
# https://www.pythonguis.com/tutorials/getting-started-flet/

import flet as ft


def main(page: ft.Page):
    page.title = "Flet Navigation Bar Demo"
    page.window.width = 360
    page.window.height = 260

    info = ft.Text("You are on the Home tab")

    def on_nav_change(e):
        idx = page.navigation_bar.selected_index
        if idx == 0:
            info.value = "You are on the Home tab"
        elif idx == 1:
            info.value = "You are on the Search tab"
        else:
            info.value = "You are on the Profile tab"
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Search"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Profile"),
        ],
        on_change=on_nav_change,
    )

    page.add(
        ft.Container(content=info, alignment=ft.alignment.center, padding=20),
    )


ft.app(target=main)
