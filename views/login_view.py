import flet as ft
from controllers.login_controller import LoginController

def main(page: ft.Page):
    def login_click(e):
        username = txt_username.value
        password = txt_password.value
        controller = LoginController()
        user_info = controller.login(username, password)
        if user_info:
            page.clean()
            if user_info['role'] == 'volunteer':
                page.add(ft.Text(f"Welcome, {user_info['name']}!"))
                page.add(ft.Text(f"Specialization: {user_info['specialization']}"))
            else:
                page.add(ft.Text("Welcome Admin!"))  # Add admin-specific UI here
        else:
            page.add(ft.Text("Login Failed. Please try again."))

    txt_username = ft.TextField(label="Username")
    txt_password = ft.TextField(label="Password", password=True)
    btn_login = ft.ElevatedButton("Login", on_click=login_click)

    page.add(txt_username, txt_password, btn_login)
