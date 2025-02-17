import flet as ft
from controllers.login_controller import LoginController

def user_view(page: ft.Page, user_data):
    page.title = 'Gardenia - Volunteer Dashboard'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = 'dark'

    title = ft.Text("VOLUNTEER DASHBOARD", size=30, weight=ft.FontWeight.BOLD, color='#77DD77')
    
    # Ensure 'username' exists in user_data
    if 'username' not in user_data:
        page.add(ft.Text("Error: Username not found. Please contact support.", color="red"))
        return

    # Welcome message with name and specialization
    welcome_msg = ft.Text(
        value=f"Welcome, {user_data.get('name', 'Volunteer')}!",
        size=20,
        color='#77DD77'
    )
    specialization_msg = ft.Text(
        value=f"Your specialization is assigned to: {user_data.get('specialization', 'Not Assigned')}",
        size=18,
        color='white'
    )
    
    txt_new_password = ft.TextField(label="New Password", password=True, width=500, border_color='white')
    result = ft.Text()

    def update_password_click(e):
        new_password = txt_new_password.value
        controller = LoginController()
        try:
            if controller.update_password(user_data['username'], new_password):
                result.value = "Password updated successfully."
            else:
                result.value = "Failed to update password. Please try again."
        except KeyError as ke:
            result.value = "An error occurred: " + str(ke)
        except Exception as e:
            result.value = "An unexpected error occurred: " + str(e)
        page.update()

    btn_update_password = ft.ElevatedButton(text="Update Password", color='#77DD77', on_click=update_password_click)

    def go_back(e):
        page.views.pop()
        page.update()

    back_button = ft.TextButton(text="Back to Login", on_click=go_back)

    page.add(
        ft.Column(
            [
                title,
                welcome_msg,
                ft.Text(value="\n"),
                specialization_msg,
                ft.Text(value="\n\n"),
                txt_new_password,
                btn_update_password,
                back_button,
                result
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.views.append(user_view)
    page.update()
