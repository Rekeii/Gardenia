import flet as ft
from models.user_model import UserModel
from controllers.volunteer_controller import VolunteerController
from controllers.plant_controller import PlantController
from models.plant_model import PlantModel, PlantType, PlantHealth
from models.volunteer_model import Volunteer, Specialization, TaskStatus
from views.tasks_view import tasks_view
import asyncio

async def admin_view(page: ft.Page, user_info=None):
    # Ensure user_info and other necessary data is in page.data
    if not hasattr(page, 'data') or 'user_info' not in page.data:
        page.data = {'user_info': user_info}

    page.theme_mode = 'dark'

    title = ft.Container(
        content=ft.Row(
            [
                ft.Image(src="assets/qbee.png", height=30),
                ft.Text("ADMIN DASHBOARD", size=30, weight=ft.FontWeight.BOLD, color='#77DD77')
            ]
        )
    )

    # --- Volunteer Tab ---
    volunteer_controller = VolunteerController()
    volunteers = await volunteer_controller.get_all_volunteers()

    volunteer_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Username")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Specialization")),
            ft.DataColumn(ft.Text("Assigned Tasks")),
        ],
        rows=[],
    )
    user_model = UserModel()
    for volunteer in volunteers:
        # Fetch username from login collection using volunteer's user field
        # Use a space as the separator for split, and handle potential empty names
        login_info = user_model.login_collection.find_one({"user": volunteer.name.split(" ")[0] if volunteer.name else "N/A"}) # added condition here
        username = login_info.get("user", "N/A") if login_info else "N/A"

        # Fetch task names
        tasks = await volunteer_controller.get_volunteer_tasks(str(volunteer._id))
        task_names = ", ".join([task.taskName for task in tasks]) if tasks else "No tasks assigned"

        # Capitalize the specialization *for display*
        specialization_display = volunteer.specialization.value.capitalize()

        volunteer_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(username)),
                    ft.DataCell(ft.Text(volunteer.name)),
                    ft.DataCell(ft.Text(specialization_display)),  # Use the capitalized version
                    ft.DataCell(ft.Text(task_names)),
                ]
            )
        )

    volunteer_tab = ft.Container(volunteer_table)
    # --- End Volunteer Tab ---

    # --- Plant Tab ---
    plant_controller = PlantController()
    plants = await plant_controller.get_plants()

    plant_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Type")),
            ft.DataColumn(ft.Text("Planting Date")),
            ft.DataColumn(ft.Text("Harvest Date")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[],
    )

    for plant in plants:
        plant_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(plant.name)),
                    ft.DataCell(ft.Text(plant.plant_type.value)),
                    ft.DataCell(ft.Text(str(plant.planting_date.strftime('%m/%d/%Y')) if plant.planting_date else "N/A")),
                    ft.DataCell(ft.Text(str(plant.estimated_harvest_date.strftime('%m/%d/%Y')) if plant.estimated_harvest_date else "N/A")),
                    ft.DataCell(ft.Text(plant.health_status.value))
                ]
            )
        )
    plant_tab = ft.Container(plant_table)
    # --- End Plant Tab ---

    # --- User Creation Tab ---
    txt_usertab = ft.Text("User Account Creation")
    txt_username = ft.TextField(label="Username", width=500, border_color='white')
    txt_password = ft.TextField(label="Password", password=True, width=500, border_color='white')
    txt_name = ft.TextField(label="Name", width=500, border_color='white')

    specialization_options = [
        ft.dropdown.Option(
            text=specialization.value.replace("_", " ").title(),
            key=specialization.value
        )
        for specialization in Specialization
    ]

    specialization_dropdown = ft.Dropdown(
        options=specialization_options,
        value=None,
    )


    chk_is_admin = ft.Checkbox(label="Is Admin?")
    result_text = ft.Text(value="")
    
    async def create_user_handler(e):
        if not all([txt_username.value, txt_password.value, txt_name.value, specialization_dropdown.value]):
            result_text.value = "All fields are required."
            page.update()  # Remove 'await' here
            return

        username = txt_username.value
        password = txt_password.value
        name = txt_name.value
        specialization = specialization_dropdown.value.lower()
        is_admin = chk_is_admin.value
        role = 'admin' if is_admin else 'volunteer'

        try:
            success, message = user_model.create_user(username, password, name, specialization, role)
            result_text.value = message
        except Exception as err:
            print(f"Failed to create user: {err}")
            success = False
            message = f"Error creating user: {err}"
            result_text.value = message
        
        if success:
            # Reset form fields
            txt_username.value = ""
            txt_password.value = ""
            txt_name.value = ""
            specialization_dropdown.value = None
            chk_is_admin.value = False

            # Refresh volunteer table data
            volunteers = await volunteer_controller.get_all_volunteers()
            volunteer_table.rows.clear()
            for volunteer in volunteers:
                tasks = await volunteer_controller.get_volunteer_tasks(str(volunteer._id))
                task_names = ", ".join([task.taskName for task in tasks]) if tasks else "No tasks assigned"
                volunteer_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(volunteer.user)),
                            ft.DataCell(ft.Text(volunteer.name)),
                            ft.DataCell(ft.Text(volunteer.specialization.value.capitalize())),
                            ft.DataCell(ft.Text(task_names)),
                        ]
                    )
                )

        # Update the page after changes
        page.update()  # Remove 'await' here
    # Use the outer page variable here

    # Tasks Tab
    tasks_tab_content = await tasks_view(page, volunteer_controller)


    user_tab = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        txt_usertab,
                        txt_username,
                        txt_password,
                        txt_name,
                        specialization_dropdown,
                        chk_is_admin,
                        ft.ElevatedButton(
                            text="Create User",
                            color='#77DD77',
                            on_click=create_user_handler,
                        ),
                        result_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )
    # --- End User Creation Tab ---

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Volunteers", icon="PEOPLE", content=volunteer_tab),
            ft.Tab(text="Create User", icon="PERSON_ADD", content=user_tab),
            ft.Tab(text="Plants", icon="GRASS", content=plant_tab),
            ft.Tab(text="Tasks", icon="TASK", content=tasks_tab_content),
        ],
        expand=1,
    )

    admin_dashboard = ft.View(
        "/admin",
        controls=[
            title,
            tabs,
            ft.TextButton(
                text="Back to Login",
                on_click=lambda e: asyncio.run(go_back(page))
            )
        ]
    )

    page.views.append(admin_dashboard)
    page.update()

async def go_back(page: ft.Page):
    if len(page.views) > 1:
        page.views.pop()

    from views.login_view import login_view
    await login_view(page)
    page.update()

# Modify the task table section in tasks_tab_content
async def refresh_task_table(task_table, volunteers):
    tasks = await volunteer_controller.get_all_tasks()
    task_table.rows.clear()
    
    for task in tasks:
        # Find assigned volunteer name
        volunteer_name = "Unassigned"
        if task.assignedVolunteerId:
            volunteer = next(
                (v for v in volunteers if str(v._id) == task.assignedVolunteerId),
                None
            )
            volunteer_name = volunteer.name if volunteer else "Unknown"

        # Only show non-completed tasks in admin view
        if task.status != TaskStatus.Completed.value:
            task_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(task.taskName)),
                        ft.DataCell(ft.Text(task.frequency.value.title())),
                        ft.DataCell(ft.Text(volunteer_name)),
                        ft.DataCell(ft.Text(task.status.value)),
                    ]
                )
            )

# Update the volunteer table refresh function
async def refresh_volunteer_table(volunteer_table):
    volunteers = await volunteer_controller.get_all_volunteers()
    volunteer_table.rows.clear()
    
    for volunteer in volunteers:
        # Only get non-completed tasks
        tasks = await volunteer_controller.get_volunteer_tasks(str(volunteer._id))
        active_tasks = [task for task in tasks if task.status != TaskStatus.Completed.value]
        task_names = ", ".join([task.taskName for task in active_tasks]) if active_tasks else "No active tasks"

        login_info = user_model.login_collection.find_one({"user": volunteer.name.split(" ")[0] if volunteer.name else "N/A"})
        username = login_info.get("user", "N/A") if login_info else "N/A"

        volunteer_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(username)),
                    ft.DataCell(ft.Text(volunteer.name)),
                    ft.DataCell(ft.Text(volunteer.specialization.value.capitalize())),
                    ft.DataCell(ft.Text(task_names)),
                ]
            )
        )
