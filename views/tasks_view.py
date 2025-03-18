import flet as ft
from controllers.volunteer_controller import VolunteerController
from models.volunteer_model import Volunteer
import asyncio

async def tasks_view(page: ft.Page, volunteer_controller: VolunteerController) -> ft.Container:
    # Fetch volunteers and tasks
    volunteers = await volunteer_controller.get_all_volunteers()
    tasks = await volunteer_controller.get_all_tasks()

    
    # Task Creation Form Components
    create_task_result = ft.Text()
    txt_task_name = ft.TextField(label="Task Name", width=500, border_color='white')
    frequency_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(text="Daily", key="daily"),
            ft.dropdown.Option(text="Monthly", key="monthly"),
        ],
        value="daily",  # Default to Daily
    )
    assigned_volunteer_dropdown = ft.Dropdown(
        label="Assign to Volunteer",
        options=[
            ft.dropdown.Option(text=volunteer.name, key=str(volunteer._id))
            for volunteer in volunteers
        ],
        value=None,  # Optional assignment
    )

    async def create_task_handler(e):
        task_name = txt_task_name.value
        frequency = frequency_dropdown.value
        volunteer_id = assigned_volunteer_dropdown.value  # Can be None

        if not task_name:
            create_task_result.value = "Task name is required."
            page.update()
            return

        try:
            success, message = await volunteer_controller.add_task(
                task_name, frequency, volunteer_id
            )
            create_task_result.value = message
        except Exception as err:
            create_task_result.value = f"Error: {err}"
            page.update()
            return

        # Clear form fields
        txt_task_name.value = ""
        assigned_volunteer_dropdown.value = None

        # Refresh tasks table
        tasks = await volunteer_controller.get_all_tasks()
        task_table.rows.clear()
        for task in tasks:
            volunteer_name = "Unassigned"
            if task.assignedVolunteerId:
                volunteer = next(
                    (
                        v
                        for v in volunteers
                        if str(v._id) == task.assignedVolunteerId
                    ),
                    None,
                )
                volunteer_name = volunteer.name if volunteer else "Unknown"

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
        page.update()

    # Task Table
    task_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Task Name")),
            ft.DataColumn(ft.Text("Frequency")),
            ft.DataColumn(ft.Text("Assigned To")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[],
    )

    # Initialize task_table with existing tasks
    for task in tasks:
        volunteer_name = "Unassigned"
        if task.assignedVolunteerId:
            volunteer = next(
                (
                    v
                    for v in volunteers
                    if str(v._id) == task.assignedVolunteerId
                ),
                None,
            )
            volunteer_name = volunteer.name if volunteer else "Unknown"

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

    return ft.Container(
        ft.Column(
            [
                ft.Text("Create New Task"),
                txt_task_name,
                frequency_dropdown,
                assigned_volunteer_dropdown,
                ft.ElevatedButton(
                    text="Create Task",
                    color='#77DD77',
                    on_click=create_task_handler,
                ),
                create_task_result,
                ft.Text("All Tasks", size=18),
                task_table,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        padding=20,
    )
