import flet as ft
from controllers.login_controller import LoginController

def user_view(page: ft.Page, user_data):
    
    # Set theme mode for the page
    page.theme_mode = 'dark'
    
    # Create controls
    title = ft.Container(
        content=ft.Row(
            [
                ft.Image(src="Gardenia-main/assets/Bee.png", height=30), 
                ft.Text("VOLUNTEER DASHBOARD", size=30, weight=ft.FontWeight.BOLD, color='#77DD77')
            ]
        )
    )
    
    ## Plant Management Tab
    plant_table = ft.DataTable(
        width=1500,
        height=700,
        data_row_max_height=60,
        bgcolor="#192142",
        border=ft.border.all(2, "white"),
        border_radius=10,
        columns=[
            ft.DataColumn(ft.Text("Name and Type")),
            ft.DataColumn(ft.Text("Dates")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Plant Log")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Column([ft.Text("Bulbasaur"), ft.Text("Shrub")]), show_edit_icon=True),
                    ft.DataCell(ft.Column([ft.Text("Planted on: ##/##/##"), ft.Text("Harvest Date: ##/##/##")]), show_edit_icon=True),
                    ft.DataCell(ft.Text("NonExistent"), show_edit_icon=True),
                    ft.DataCell(ft.Text("Dear Diary..."), show_edit_icon=True),
                ],
            ),
        ],
    )

    # Function to add new row
    def add_row(e):
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Column([ft.Text("New Plant"), ft.Text("Type: ")]), show_edit_icon=True),
                ft.DataCell(ft.Column([ft.Text("Planted on: ##/##/##"), ft.Text("Harvest Date: ##/##/##")]), show_edit_icon=True),
                ft.DataCell(ft.Text("Pending"), show_edit_icon=True),
                ft.DataCell(ft.Text("Enter Log Entry"), show_edit_icon=True),
            ],
        )
        # Insert before last row (which contains the button)
        plant_table.rows.insert(len(plant_table.rows) - 1, new_row)
        page.update()

    # Plant Seed button
    plant_seed = ft.FilledButton(
        text="Plant Seed",
        bgcolor='#9ae69a', 
        icon='add',
        on_click=add_row
    )

    # Add the button row at the end
    plant_table.rows.append(
        ft.DataRow(
            cells=[
                ft.DataCell(content=plant_seed),
                ft.DataCell(ft.Text(" ")),
                ft.DataCell(ft.Text(" ")),
                ft.DataCell(ft.Text(" ")),
            ],
        )
    )

    plant_tab = ft.Column([plant_table], scroll=True)

    ## User Tab
    welcome_msg = ft.Text(value=f"Welcome, {user_data.get('name', 'Volunteer')}!", size=20, color='#77DD77')
    specialization_msg = ft.Text(value=f"Specialization: {user_data.get('specialization', 'Not Assigned')}", size=18, color='white')
    txt_new_password = ft.TextField(label="New Password", password=True, width=500, border_color='white')
    result = ft.Text(value="")
    
    user_tab = ft.Column(
        [
            welcome_msg,
            ft.Text(value="\n"),
            specialization_msg,
            ft.Text(value="\n\n"),
            txt_new_password,
            ft.ElevatedButton(
                text="Update Password",
                color='#77DD77',
                on_click=lambda e: update_password(volunteer_dashboard, txt_new_password, result)
            ),
            result
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    #Compile Tabs
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,
        tabs=[
            ft.Tab(text="Plant Management", content=plant_tab),
            ft.Tab(text="User Management", content=user_tab),
            ft.Tab(text="Others", content=ft.Text("To be added"))
        ],
        expand=1
    )

    # Create the main view
    volunteer_dashboard = ft.View(
        "/user",
        controls=[
                title,
                tabs,
                ft.TextButton(
                    text="Back to Login",
                    on_click=lambda e: go_back(page)
                )
            ]
    )
    
    # Add the view to the page
    page.views.append(volunteer_dashboard)
    page.update()



def update_password(volunteer_dashboard, txt_new_password, result):
    new_password = txt_new_password.value
    controller = LoginController()
    username = volunteer_dashboard.page.data['user_data']['username']
    success, message = controller.update_password(username, new_password)
    result.value = message

    #clear text field after updating
    if success:
        txt_new_password.value = ""

    volunteer_dashboard.page.update()

def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()

    from views.login_view import login_view
    login_view(page)  
    page.update()
