import flet as ft
from views.login_view import login_view
from views.admin_view import admin_view
from views.user_view import user_view
from views.addplant_view import add_plant_view

async def main(page: ft.Page):
    async def route_change(route):
        if page.route == "/login":
            await login_view(page)
        elif page.route == "/admin":
            await admin_view(page, page.data)
        elif page.route == "/user":
            await user_view(page, page.data)
        elif page.route == "/add_plant":
            await add_plant_view(page)

    page.on_route_change = route_change
    page.route = "/login"  # Always start on login
    page.update()

ft.app(target=main)
