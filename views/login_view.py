import flet as ft
from controllers.login_controller import LoginController
from views.admin_view import admin_view
from views.user_view import user_view
import asyncio

async def login_view(page: ft.Page):
    # Initialize login data
    login_data = {
        'username': '',
        'password': ''
    }

    page.theme_mode = 'dark'

    # Use a dedicated ft.Text control for error messages
    error_text = ft.Text(value="", color="red")

    # Background Image Container
    bg_image = ft.Container(
        ft.Row([
            ft.Image(src="bg.png", fit=ft.ImageFit.CONTAIN),
            ft.Image(src="bg.png", fit=ft.ImageFit.CONTAIN),
        ])
    )

    # Login Interface
    login_interface = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src="assets/plant.png", height=100),
                        ft.Text("GARDENIA", size=100, weight=ft.FontWeight.BOLD, color='#77DD77'),
                        ft.Image(src="assets/grass.png", height=100)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.TextField(
                    label="Username",
                    width=500,
                    border_color='white',
                    on_change=lambda e: login_data.update({'username': e.control.value})
                ),
                ft.TextField(
                    label="Password",
                    password=True,
                    width=500,
                    border_color='white',
                    on_change=lambda e: login_data.update({'password': e.control.value})
                ),
                ft.ElevatedButton(
                    text="Login",
                    color='#77DD77',
                    on_click=lambda e: asyncio.run(login_click(login_data, page, error_text))
                ),
                error_text  # Show error message below button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["transparent", "#D9000000", "black", "#D9000000", "transparent"]
        ),
        expand=True
    )

    # Stack everything together
    page.views.append(
        ft.View(
            "/login",
            controls=[
                ft.Stack([
                    bg_image,        # Background Image
                    login_interface   # Login Box
                ], expand=True)
            ]
        )
    )
    page.update()  # Await page.update()


async def login_click(login_data, page, error_text):  # Make login_click async
    controller = LoginController()
    user_info = controller.login(login_data['username'], login_data['password'])
    if user_info:
        # For volunteers, ensure we get the volunteer ID from MongoDB
        if user_info['role'] != 'admin':
            volunteer = controller.user_model.volunteers_collection.find_one({'user': login_data['username']})
            if volunteer:
                user_info['_id'] = str(volunteer['_id'])
            else:
                error_text.value = "Error: Volunteer record not found"
                page.update()  # Remove await here
                return

        # Clear current views except login
        while len(page.views) > 1:
            page.views.pop()
            
        # Store user info for navigation
        page.data = user_info
        page.data['user_data'] = user_info
        
        # Navigate to appropriate view
        if user_info['role'] == 'admin':
            await admin_view(page, user_info)
        else:
            await user_view(page, user_info)
            
        page.update()  # Remove await here
        error_text.value = ""
    else:
        error_text.value = "Invalid username or password"
        page.update()  # Remove await here

