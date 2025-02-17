import flet as ft
from controllers.login_controller import LoginController

def user_view(page: ft.Page, user_data):
    # Ensure user_data is available in page.data
    if 'user_data' not in page.data:
        page.data['user_data'] = user_data
    
    # Set theme mode for the page
    page.theme_mode = 'dark'
    
    # Create controls
    title = ft.Text("VOLUNTEER DASHBOARD", size=30, weight=ft.FontWeight.BOLD, color='#77DD77')
    welcome_msg = ft.Text(
        value=f"Welcome, {user_data.get('name', 'Volunteer')}!",
        size=20,
        color='#77DD77'
    )
    specialization_msg = ft.Text(
        value=f"Specialization: {user_data.get('specialization', 'Not Assigned')}",
        size=18,
        color='white'
    )
    txt_new_password = ft.TextField(
        label="New Password",
        password=True,
        width=500,
        border_color='white'
    )
    result = ft.Text(value="")
    
    # Create the main view
    volunteer_dashboard = ft.View(
        "/user",
        controls=[
            title,
            welcome_msg,
            ft.Text(value="\n"),
            specialization_msg,
            ft.Text(value="\n\n"),
            txt_new_password,
            ft.ElevatedButton(
                text="Update Password",
                color='#77DD77',
                on_click=lambda e: update_password(volunteer_dashboard, txt_new_password)
            ),
            ft.TextButton(
                text="Back to Login",
                on_click=lambda e: go_back(page)
            ),
            result
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Add the view to the page
    page.views.append(volunteer_dashboard)
    page.update()

def update_password(volunteer_dashboard, txt_new_password):
    new_password = txt_new_password.value
    controller = LoginController()
    username = volunteer_dashboard.page.data['user_data']['username']
    success, message = controller.update_password(username, new_password)
    volunteer_dashboard.controls[-1].value = message
    volunteer_dashboard.page.update()

def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()
        page.update()
