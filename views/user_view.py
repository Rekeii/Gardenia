# views/user_view.py (Modified)
import flet as ft
from controllers.login_controller import LoginController
from controllers.plant_controller import PlantController
from models.plant_model import PlantModel
import asyncio
from views.plant_log_view import plant_log_view  # Import the new view


async def user_view(page: ft.Page, user_data):
    page.theme_mode = 'dark'

    title = ft.Container(
        content=ft.Row(
            [
                ft.Image(src="assets/bee.png", height=30),
                ft.Text("VOLUNTEER DASHBOARD", size=30, weight=ft.FontWeight.BOLD, color='#77DD77')
            ]
        )
    )

    plant_controller = PlantController()
    plants = await plant_controller.get_plants()

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
        rows=[]
    )

    for plant in plants:
        # Get the latest observation, handling empty lists and missing colons safely
        if plant.observations:
            last_obs = plant.observations[-1]
            parts = last_obs.split(":", 1)  # Split only once
            if len(parts) > 1:
                latest_observation = parts[1].strip()  # Get the part after the colon
            else:
                latest_observation = last_obs  # Use the whole string if no colon
        else:
            latest_observation = "No Log Entries"
        # Get id
        plant_id_str = str(plant._id)

        async def show_plant_log(e, plant_id=plant_id_str): #added ID
            """Navigates to the plant_log_view with the plant's ID."""
            await plant_log_view(page, plant_id) # Await to display page



		# Add rows into the table
        plant_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Column([ft.Text(plant.name), ft.Text(plant.plant_type.value)])),
                    ft.DataCell(ft.Column([ft.Text(f"Planted on: {plant.planting_date.strftime('%m/%d/%Y')}" if plant.planting_date else "Planted on: N/A"),
                                            ft.Text(f"Harvest Date: {plant.estimated_harvest_date.strftime('%m/%d/%Y')}" if plant.estimated_harvest_date else "Harvest Date: N/A")])),
                    ft.DataCell(ft.Text(plant.health_status.value)),
                    ft.DataCell(
                        ft.TextButton(latest_observation, on_click=lambda e, plant_id=plant_id_str: asyncio.run(show_plant_log(e, plant_id)))
                    ),
                ],
            )
        )

    def add_row(e):
        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Column([ft.Text("New Plant"), ft.Text("Type: ")]), show_edit_icon=True),
                ft.DataCell(ft.Column([ft.Text("Planted on: ##/##/##"), ft.Text("Harvest Date: ##/##/##")]), show_edit_icon=True),
                ft.DataCell(ft.Text("Pending"), show_edit_icon=True),
                ft.DataCell(ft.Text("Enter Log Entry"), show_edit_icon=True),
            ],
        )
        plant_table.rows.insert(len(plant_table.rows) - 1, new_row)
        page.update()

    plant_seed = ft.FilledButton(
        text="Plant Seed",
        bgcolor='#9ae69a',
        icon='add',
        on_click=add_row
    )

    plant_table.rows.append(
        ft.DataRow(
            cells=[
                ft.DataCell(content=plant_seed),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
            ],
        )
    )

    plant_tab = ft.Column([plant_table], scroll=ft.ScrollMode.AUTO)

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
                on_click=lambda e: asyncio.run(update_password(volunteer_dashboard, txt_new_password, result))
            ),
            result
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,
        tabs=[
            ft.Tab(icon="GRASS",content=plant_tab),
            ft.Tab(icon="KEY_SHARP", content=user_tab),
            ft.Tab(icon="CONSTRUCTION_SHARP", content=ft.Text("To be added")),
            ft.Tab(icon="INVENTORY", content=ft.Text("To be added")),
        ],
        expand=1
    )


    volunteer_dashboard = ft.View(
        "/user",
        controls=[
                title,
                tabs,
                ft.TextButton(
                    text="Back to Login",
                    on_click=lambda e: asyncio.run(go_back(page))
                )
            ]
    )



    page.views.append(volunteer_dashboard)
    page.update()

async def update_password(volunteer_dashboard, txt_new_password, result):
    new_password = txt_new_password.value
    controller = LoginController()
    username = volunteer_dashboard.page.data['user_data']['username']
    success, message = await controller.update_password(username, new_password)
    result.value = message

    if success:
        txt_new_password.value = ""

    await volunteer_dashboard.page.update()

async def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()

    from views.login_view import login_view
    await login_view(page)
    page.update()

