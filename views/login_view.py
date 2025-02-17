import flet as ft
from controllers.login_controller import LoginController
from views.admin_view import admin_view
from views.user_view import user_view

def login_view(page: ft.Page):
    page.title = 'Gardenia Login'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = 'dark'

    title = ft.Text("GARDENIA", size=100, weight=ft.FontWeight.BOLD, color='#77DD77')
    username = ft.TextField(label="Username", width=500, border_color='white')
    password = ft.TextField(label="Password", password=True, width=500, border_color='white')
    result = ft.Text()

    def login_click(e):
        controller = LoginController()
        user_info = controller.login(username.value, password.value)
        if user_info:
            page.clean()
            if user_info['role'] == 'admin':
                admin_view(page)
            else:
                user_view(page, user_info)  # Pass the entire user_info to user_view
            page.update()
        else:
            result.value = "Invalid username or password"
            page.update()


    login_button = ft.ElevatedButton(text="Login", color='#77DD77', on_click=login_click)

    def changepassword(e):
        change_username = ft.TextField(label="Username", width=500, border_color='white')
        new_password = ft.TextField(label="New Password", password=True, width=500, border_color='white')
        change_result = ft.Text()

        def submit_new_password(e):
            username = change_username.value
            password = new_password.value
            controller = LoginController()
            if controller.update_password(username, password):
                change_result.value = f"Password for {username} has been updated."
            else:
                change_result.value = "Failed to update password. Please try again."
            page.update()

        def go_back(e):
            page.views.pop()
            page.update()

        page.views.append(
            ft.View(
                "/change_password",
                controls=[
                    ft.Text("Change Password", size=30, color='#77DD77'),
                    change_username,
                    new_password,
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Submit", color='#77DD77', on_click=submit_new_password),
                            ft.TextButton(text="Back", on_click=go_back)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    change_result
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    changepass_button = ft.TextButton(text="Change Password", on_click=changepassword)

    page.add(
        ft.Column(
            [title, username, password, ft.Row([login_button, changepass_button], alignment=ft.MainAxisAlignment.CENTER), result],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
