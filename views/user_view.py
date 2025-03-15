# views/user_view.py (Revised)
import flet as ft
from controllers.login_controller import LoginController
from controllers.plant_controller import PlantController
from models.plant_model import PlantModel, PlantHealth
from views.plant_log_view import plant_log_view
from views.inventory_view import inventory_view
from views.addplant_view import add_plant_view  
import asyncio


async def user_view(page: ft.Page, user_data):
    page.data = {"user_data": user_data}
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
    async def refresh_plants_table():
        plants = await plant_controller.get_plants()
        plant_table.rows.clear()
        
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

            status_options = [
                ft.dropdown.Option(
                    text=status.value.replace("_", " ").title(),
                    key=status.value
                )
                for status in PlantHealth
            ]

            status_dropdown = ft.Dropdown(
                data=plant_id_str,
                options=status_options,
                value=plant.health_status.value,
                on_change=handle_status_change
            )

            plant_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Column([
                            ft.Text(plant.name),
                            ft.Text(plant.plant_type.value)
                        ])),
                        ft.DataCell(ft.Column([
                            ft.Text(f"Planted on: {plant.planting_date.strftime('%m/%d/%Y')}" 
                                    if plant.planting_date else "Planted on: N/A"),
                            ft.Text(f"Harvest Date: {plant.estimated_harvest_date.strftime('%m/%d/%Y')}" 
                                    if plant.estimated_harvest_date else "Harvest Date: N/A")
                        ])),
                        ft.DataCell(status_dropdown),
                        ft.DataCell(
                            ft.TextButton(latest_observation, 
                                          on_click=lambda e, 
                                          plant_id=plant_id_str: asyncio.run(show_plant_log(e, plant_id)))
                        ),
                    ]
                )
            )
        page.update()

    async def handle_status_change(e):
        try:
            plant_id = e.control.data
            new_status = PlantHealth(e.control.value)
            
            success, msg = await plant_controller.update_plant_health(plant_id, new_status)
            if success:
                print("Status updated successfully")
                await refresh_plants_table()
            else:
                e.control.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error: {msg}"),
                    action="OK"
                )
                e.control.page.update()
                
        except Exception as e:
            print(f"Error: {str(e)}")
            e.control.page.snack_bar = ft.SnackBar(
                content=ft.Text("Failed to update status"),
                action="OK"
            )
            e.control.page.update()


    await refresh_plants_table()

    plant_seed = ft.FilledButton(
        text="Plant Seed",
        bgcolor='#9ae69a',
        icon='add',
       on_click=lambda e: page.go("/add_plant")
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

    # Rest of your existing code remains unchanged below this line
    welcome_msg = ft.Text(value=f"Welcome, {user_data.get('name', 'Volunteer')}!", size=20, color='#77DD77')
    specialization_msg = ft.Text(value=f"Specialization: {user_data.get('specialization', 'Not Assigned')}", size=18, color='white')
    
    # Password update section remains unchanged
    login_controller = LoginController()
    result = ft.Text()
    txt_new_password = ft.TextField(label="New Password", password=True, width=500)

    def update_password_handler(e):
        new_password = txt_new_password.value.strip()
        if not new_password:
            result.value = "Password cannot be empty"
            result.color = ft.colors.RED
        else:
            try:
                success, msg = asyncio.run(login_controller.update_password(
                    username=user_data['username'],
                    new_password=new_password
                ))
                if success:
                    result.value = "Password updated successfully!"
                    result.color = ft.colors.GREEN
                    txt_new_password.value = ""
                else:
                    result.value = msg
                    result.color = ft.colors.RED
            except Exception as ex:
                result.value = f"Error: {str(ex)}"
                result.color = ft.colors.RED
        page.update()

    async def handle_back_button(e):
        if len(page.views) > 1:
            page.views.pop()
        await login_view(page)
        page.update()

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
                on_click=update_password_handler
            ),
            result
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    inventory_tab = await inventory_view(page, user_data)
    
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,
        tabs=[
            ft.Tab(icon="GRASS",content=plant_tab),
            ft.Tab(icon="KEY_SHARP", content=user_tab),
            ft.Tab(icon="CONSTRUCTION_SHARP", content=ft.Text("To be added")),
            ft.Tab(icon="INVENTORY", content=inventory_tab),
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

async def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()

    from views.login_view import login_view
    await login_view(page)
    page.update()
