import flet as ft
from controllers.admin_controller import AdminController

def admin_view(page: ft.Page):
    page.title = 'Gardenia - Admin Dashboard'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = 'dark'

    title = ft.Text("ADMIN DASHBOARD", size=50, weight=ft.FontWeight.BOLD, color='#77DD77')
    
    txt_username = ft.TextField(label="Username", width=500, border_color='white')
    txt_password = ft.TextField(label="Password", password=True, width=500, border_color='white')
    txt_name = ft.TextField(label="Name", width=500, border_color='white')
    txt_specialization = ft.TextField(label="Specialization", width=500, border_color='white')
    chk_is_admin = ft.Checkbox(label="Is Admin?", width=500)
    result = ft.Text()

    def create_user_click(e):
        username = txt_username.value
        password = txt_password.value
        name = txt_name.value
        specialization = txt_specialization.value
        role = 'admin' if chk_is_admin.value else 'volunteer'

        controller = AdminController()
        success, message = controller.create_user(username, password, name, specialization, role)
        result.value = message
        page.update()

    btn_create_user = ft.ElevatedButton(text="Create User", color='#77DD77', on_click=create_user_click)

    def go_back(e):
        page.views.pop()
        page.update()

    back_button = ft.TextButton(text="Back to Login", on_click=go_back)

    page.add(
        ft.Column(
            [
                title,
                txt_username,
                txt_password,
                txt_name,
                txt_specialization,
                chk_is_admin,
                btn_create_user,
                back_button,
                result
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.views.append(admin_view)
    page.update()