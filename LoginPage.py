import flet as ft
from flet import TextField


def main(page: ft.Page):
    page.title = 'Gardenia'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = 'dark'

    title = ft.Text("GARDENIA", size=100, weight=ft.FontWeight.BOLD, color='#77DD77')
    username = ft.TextField(label="Username", width=500, border_color='white')
    password = ft.TextField(label="Password", password=True, width=500, border_color='white')
    result = ft.Text()

    def login(e):
        user = controller.authenticateUser(username.value, password.value)
        result.value = f"Login successful! Welcome {user.username}" if user else "Invalid username or password"
        page.update()

    login_button = ft.ElevatedButton(text="Login", color='green', on_click=login)

    def changepassword(e):
        change_username = ft.TextField(label="Username", width=500, border_color='white')
        new_password = ft.TextField(label="New Password", password=True, width=500, border_color='white')
        change_result = ft.Text()

        def submit_new_password(e):
            # Here you can add logic to update the password
            change_result.value = f"Password for {change_username.value} has been updated."
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
                            ft.ElevatedButton(text="Submit", color='green', on_click=submit_new_password),
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
            [title, username, password, ft.Row([login_button, changepass_button], alignment=ft.MainAxisAlignment.CENTER),result],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == '__main__':
    ft.app(target=main)
