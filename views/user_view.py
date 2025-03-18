import flet as ft
from controllers.login_controller import LoginController
from controllers.plant_controller import PlantController
from controllers.volunteer_controller import VolunteerController
from models.plant_model import PlantModel, PlantHealth
from models.volunteer_model import Volunteer, TaskStatus
from views.plant_log_view import plant_log_view
from views.inventory_view import inventory_view
from views.addplant_view import addplant_view  # Make sure this import is here
import asyncio
from controllers.weather_controller import WeatherController

async def user_view(page: ft.Page, user_data):
    # Ensure user_data contains '_id'
    if '_id' not in user_data:
        raise KeyError("Volunteer ID '_id' not found in user_data")

    volunteer_id = user_data['_id']
    print(f"Volunteer ID: {volunteer_id}")  # Debug print statement

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
           
            if plant.observations:
                last_obs = plant.observations[-1]
                parts = last_obs.split(":", 1)  
                if len(parts) > 1:
                    latest_observation = parts[1].strip()  
                else:
                    latest_observation = last_obs  
            else:
                latest_observation = "No Log Entries"
            
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
    
    
    async def route_change(e):
        if page.route == "/add_plant":
            add_view = await addplant_view(page)  # Store the returned view
            page.views.append(add_view)  # Append the view
            await page.update_async()  # Update the page
        elif page.route == "/user":
            await user_view(page, user_data)
        page.update()

    page.on_route_change = route_change

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.route = top_view.route
        page.update()

    # Assign handlers
    #page.on_route_change = route_change
    #page.on_view_pop = view_pop
    
    async def route_change(e):
        if page.route == "/add_plant":
            await addplant_view(page)  
        elif page.route == "/user":
            # Rebuild user view to refresh data
            await user_view(page, user_data)
        page.update()

    page.on_route_change = route_change

    # Add "Plant Seed" button
    async def go_to_add_plant(e):
        add_view = await addplant_view(page)
        page.views.append(add_view)
        await page.update_async()

    plant_seed = ft.FilledButton(
        text="Plant Seed",
        bgcolor='#9ae69a',
        icon='add',
        on_click=lambda _: page.go("/add_plant")  # Direct route navigation
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
    
    refresh = ft.IconButton(icon="REFRESH", on_click=page.update())

    plant_tab = ft.Column([plant_table], scroll=ft.ScrollMode.AUTO)

    welcome_msg = ft.Text(value=f"Welcome, {user_data.get('name', 'Volunteer')}!", size=20, color='#77DD77')
    specialization_msg = ft.Text(value=f"Specialization: {user_data.get('specialization', 'Not Assigned')}", size=18, color='white')
    
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
        await login_view(page) # type: ignore
        page.update()
      
      
    # TASKS USER_TAB  
    volunteer_controller = VolunteerController()
    tasks = await volunteer_controller.get_volunteer_tasks(volunteer_id)

    # Separate tasks into pending and completed
    pending_tasks = [task for task in tasks if task.status != TaskStatus.Completed.value]
    completed_tasks = [task for task in tasks if task.status == TaskStatus.Completed.value]

    async def handle_complete_task(e, task_id: str):
        success, msg = await volunteer_controller.mark_task_complete(task_id)
        if success:
            # Simply update the page route to refresh
            page.go("/user")
            page.update()

    # Create lists for pending and completed tasks
    pending_task_buttons = []
    for task in pending_tasks:
        task_id = str(task._id)
        created_date = task.created_at.strftime("%Y-%m-%d %H:%M") if task.created_at else "Unknown"
        button_container = ft.Column([
            ft.ElevatedButton(
                text=task.taskName,
                color="#77DD77",
                on_click=lambda e, tid=task_id: asyncio.run(handle_complete_task(e, tid)),
                style=ft.ButtonStyle(
                    padding=10,
                    bgcolor="#192142",
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            ft.Text(
                f"Created: {created_date}",
                color="#808080",
                size=12,
                italic=True
            )
        ])
        pending_task_buttons.append(button_container)

    completed_task_texts = []
    for task in completed_tasks:
        completed_date = task.completed_at.strftime("%Y-%m-%d %H:%M") if task.completed_at else "Unknown"
        created_date = task.created_at.strftime("%Y-%m-%d %H:%M") if task.created_at else "Unknown"
        text = ft.Column([
            ft.Text(
                f"✓ {task.taskName}",
                color="#4CAF50",
                size=16,
                italic=True
            ),
            ft.Text(
                f"Created: {created_date}",
                color="#808080",
                size=12,
                italic=True
            ),
            ft.Text(
                f"Completed: {completed_date}",
                color="#808080",
                size=12,
                italic=True
            ),
        ])
        completed_task_texts.append(text)

    # Construct the dynamic task list UI with two sections
    user_tasks = ft.Column(
        [
            ft.Text("TASK LIST", size=50, weight=ft.FontWeight.BOLD, color='#77DD77'),
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Pending Tasks", size=24, weight=ft.FontWeight.BOLD, color='#77DD77'),
                        ft.Column(
                            pending_task_buttons,
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO
                        ) if pending_task_buttons else ft.Text("No pending tasks", color='white', italic=True),
                        ft.Divider(height=2, color='#77DD77'),
                        ft.Text("Completed Tasks", size=24, weight=ft.FontWeight.BOLD, color='#77DD77'),
                        ft.Column(
                            completed_task_texts,
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO
                        ) if completed_task_texts else ft.Text("No completed tasks", color='white', italic=True),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                ),
                bgcolor="#181d30",
                padding=20,
                border_radius=10,
                expand=True
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    weather_controller = WeatherController()
    weather_text = ft.Text("Loading weather...", color='white', size=16)

    async def update_weather():
        try:
            weather = await weather_controller.get_current_weather()
            weather_text.value = f"Current weather: {weather.condition}, {weather.temperature}°C, Precipitation: {weather.precipitation}mm"
            page.update()
        except Exception as e:
            weather_text.value = "Weather data unavailable"
            print(f"Weather error: {str(e)}")
            page.update()

    await update_weather()
    
    user_settings = ft.Column(
        [
            welcome_msg,
            ft.Text(value="\n"),
            specialization_msg,
            weather_text,  # Add weather display
            ft.Text(value="\n\n"),
            txt_new_password,
            ft.ElevatedButton(
                text="Update Password",
                color='#77DD77',
                on_click=update_password_handler
            ),
            result
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Vertical center
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Horizontal center
        expand=True  # Allow column to expand and take available space
    )

    # Update the container to center its content
    user_tab = ft.Row([
        ft.Container(
            user_settings,
            bgcolor="#192142",
            expand=True,
            alignment=ft.alignment.center  # Center the content within container
        ), 
        ft.Container(
            ft.Container(user_tasks, bgcolor="#192142", expand=True),
            padding=30,
            expand=True
        )
    ], spacing=10)

    
    inventory_tab = await inventory_view(page, user_data)
    
    tabs = ft.Tabs(
        selected_index = 0,
        animation_duration= 300,
        tabs=[
            ft.Tab(text="Plants", icon="GRASS",content=plant_tab),
            ft.Tab(text="User", icon="KEY_SHARP", content=user_tab),
            ft.Tab(text="Inventory", icon="INVENTORY_SHARP", content=inventory_tab),
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
