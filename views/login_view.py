import flet as ft
from controllers.login_controller import LoginController
from views.admin_view import admin_view
from views.user_view import user_view

def login_view(page: ft.Page):
    # Initialize login data
    login_data = {
        'username': '',
        'password': ''
    }
    
    # Set theme mode for the page
    page.theme_mode = 'dark'
    
    login_interface = ft.View(
        "/login",
        controls=[
            ft.Text("GARDENIA", size=100, weight=ft.FontWeight.BOLD, color='#77DD77'),
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
                on_click=lambda e: login_click(login_data, page)
            ),
            ft.Text(value="")
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    page.views.append(login_interface)
    page.update()

def login_click(login_data, page):
    controller = LoginController()
    user_info = controller.login(login_data['username'], login_data['password'])
    if user_info:
        # Clear current views except login
        while len(page.views) > 1:
            page.views.pop()
        # Store user info for navigation
        page.data = user_info
        # Navigate to appropriate view
        if user_info['role'] == 'admin':
            admin_view(page, user_info)
        else:
            user_view(page, user_info)
        page.update()
    else:
        login_interface = page.views[0]
        login_interface.controls[-1].value = "Invalid username or password"
        page.update()
