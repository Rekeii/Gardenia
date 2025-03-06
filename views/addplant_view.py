import flet as ft
from controllers.plant_controller import PlantController  
import asyncio  

async def add_plant_view(page: ft.Page):
    print("Navigated to Add Plant Page")  # Debug print

    plant_controller = PlantController()

    name_input = ft.TextField(label="Plant Name")
    type_input = ft.TextField(label="Plant Type")
    date_input = ft.TextField(label="Planting Date (MM/DD/YYYY)")
    harvest_input = ft.TextField(label="Harvest Date (MM/DD/YYYY)")
    status_input = ft.TextField(label="Status")
    water_input = ft.TextField(label="Last Date of Watering (MM/DD/YYYY)")
    log_input = ft.TextField(label="Plant Log Entry")

    result_text = ft.Text("")

    async def save_info(e):
        new_plant = {
            "name": name_input.value,
            "plant_type": type_input.value,
            "planting_date": date_input.value,
            "estimated_harvest_date": harvest_input.value,
            "status": status_input.value,
            "last_watered": water_input.value,
            "observations": log_input.value
        }

        await plant_controller.add_plant(new_plant)  # Save to database
        result_text.value = "Plant added successfully!"
        page.update()

        await asyncio.sleep(1)
        page.route = "/user"  # Navigate back to user dashboard
        page.update()

    # Layout
    add_plant_layout = ft.Column(
        [
            ft.Text("Add a New Plant", size=24, weight=ft.FontWeight.BOLD),
            name_input, type_input, date_input, harvest_input, status_input, water_input, log_input,
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_info),
                    ft.ElevatedButton("Cancel", on_click=lambda e: page.go("/user"))
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            result_text
        ],
        tight=True
    )

    # Create the View
    add_plant_page = ft.View(
        "/add_plant",
        controls=[add_plant_layout]
    )

    page.views.append(add_plant_page)
    page.update()