import flet as ft
from controllers.login_controller import LoginController
from views.admin_view import admin_view  # Assuming you'll create this
from views.user_view import user_view

def login_view(page: ft.Page):
    # Initialize login data
    login_data = {
        'username': '',
        'password': ''
    }

    page.theme_mode = 'dark'

    # Use a dedicated ft.Text control for error messages
    error_text = ft.Text(value="")

    login_interface = ft.View(
        "/login",
        controls=[
            ft.Row(
                [
                ft.Image(src="Gardenia-main/assets/Basic.png", height=100),
                ft.Text("GARDENIA", size=100, weight=ft.FontWeight.BOLD, color='#77DD77'),
                ft.Image(src="Gardenia-main/assets/Basic2.png", height=100)
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
                on_click=lambda e: login_click(login_data, page, error_text)  # Pass error_text
            ),
            error_text  # Add the error_text control here
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.views.append(login_interface)
    page.update()


def login_click(login_data, page, error_text):  # Receive error_text
    controller = LoginController()
    user_info = controller.login(login_data['username'], login_data['password'])
    if user_info:

        # Clear current views except login
        while len(page.views) > 1:
            page.views.pop()
        # Store user info for navigation
        page.data = user_info
        # Ensure user_data is available in page.data
        page.data['user_data'] = user_info
        # Navigate to appropriate view
        if user_info['role'] == 'admin':
            admin_view(page, user_info)
        else:
            user_view(page, user_info)
        page.update()
        error_text.value = ""  # Clear any previous error
    else:
        error_text.value = "Invalid username or password"  # Set the error message
        page.update()
