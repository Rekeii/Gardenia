import flet as ft
from models.user_model import UserModel

def admin_view(page: ft.Page, user_info=None):
    # Ensure user_info is available in page.data
    if not hasattr(page, 'data') or 'user_info' not in page.data:
        page.data = {'user_info': user_info}
    
    # Set theme mode for the page
    page.theme_mode = 'dark'
    
    ## Create controls
    title = ft.Container(
        content=ft.Row(
            [
                ft.Image(src="Gardenia-main/assets/QueenBee.png", height=30), 
                ft.Text("ADMIN DASHBOARD", size=30, weight=ft.FontWeight.BOLD, color='#77DD77')
            ]
        )
    )
    
    # VolunteerTab controls
    user_model = UserModel()
    volunteers_collection = user_model.volunteers_collection
    volunteer_data = list(volunteers_collection.aggregate([
        {
            "$project": {
                "_id": 0,
                "user": "$user",
                "name": "$name",
                "specializations": "$specializations",    
                "Assigned Tasks": "$Assigned Tasks"
            }
        }
    ]))

    # Usertab controls
    txt_username = ft.TextField(label="Username", width=500, border_color='white')
    txt_password = ft.TextField(label="Password", password=True, width=500, border_color='white')
    txt_name = ft.TextField(label="Name", width=500, border_color='white')
    txt_specialization = ft.TextField(label="Specialization", width=500, border_color='white')
    chk_is_admin = ft.Checkbox(label="Is Admin?", )
    result = ft.Text(value="")
    
    ## Create Tabs
    volunteer_tab = ft.Container(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Username")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Specialization")),
                ft.DataColumn(ft.Text("Assigned Tasks")),
            ],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(item[field]))) for field in item.keys()])for item in volunteer_data]
        )
    )

    user_tab = ft.Container(
        ft.Column(
            [
                txt_username,
                txt_password,
                txt_name,
                txt_specialization,
                chk_is_admin,
                ft.ElevatedButton(
                    text="Create User",
                    color='#77DD77',
                    on_click=lambda e: create_user(txt_username, txt_password, txt_name, txt_specialization, chk_is_admin, admin_dashboard)
                ),
                result
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    
    
    ## Compile Tabs
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,
        tabs=[
            ft.Tab(text="Volunteer Management", content=volunteer_tab),
            ft.Tab(text="User Management", content=user_tab),
            ft.Tab(text="Others", content=ft.Text("To be added"))
        ],
        expand=1
    )


    # Create the main view
    admin_dashboard = ft.View(
        "/admin",
        controls=[title,
                  tabs,
                  ft.TextButton(
                        text="Back to Login",
                        on_click=lambda e: go_back(page)
                    )
                ]
    )
    
    # Add the view to the page
    page.views.append(admin_dashboard)
    page.update()

def create_user(txt_username, txt_password, txt_name, txt_specialization, chk_is_admin, admin_dashboard):
    user_model = UserModel()
    username = txt_username.value
    password = txt_password.value
    name = txt_name.value
    specialization = txt_specialization.value
    is_admin = chk_is_admin.value
    role = 'admin' if is_admin else 'volunteer'
    success, message = user_model.create_user(username, password, name, specialization, role)
    admin_dashboard.controls[-1].value = message
    admin_dashboard.page.update()

def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()
    
    from views.login_view import login_view
    login_view(page)  
    page.update()
