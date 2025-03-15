import flet as ft
from controllers.plant_controller import PlantController
from models.plant_model import PlantType, PlantHealth
import asyncio

async def add_plant_view(page: ft.Page):
    plant_controller = PlantController()

    name_input = ft.TextField(label="Plant Name")
    type_input = ft.TextField(label="Plant Type")
    date_input = ft.TextField(label="Planting Date (MM/DD/YYYY)")
    harvest_input = ft.TextField(label="Harvest Date (MM/DD/YYYY)")
    health_status_input = ft.Dropdown(
        label="Health Status",
        options=[
            ft.dropdown.Option(PlantHealth.Healthy.value),
            ft.dropdown.Option(PlantHealth.NeedsWater.value),
            ft.dropdown.Option(PlantHealth.PestsDetected.value),
            ft.dropdown.Option(PlantHealth.ReadyForHarvest.value)
        ]
    )
    location_input = ft.TextField(label="Location")
    water_input = ft.TextField(label="Last Watering Date (MM/DD/YYYY)")
    log_input = ft.TextField(label="Plant Log Entry")
    result_text = ft.Text("")

    async def save_info(e):
        new_plant = {
            "name": name_input.value,
            "plant_type": type_input.value,
            "planting_date": date_input.value,
            "estimated_harvest_date": harvest_input.value,
            "health_status": health_status_input.value,
            "location": location_input.value,
            "last_watered": water_input.value,
            "observations": log_input.value
        }

        success, message = await plant_controller.add_plant(new_plant)
        result_text.value = message

        if success:
            name_input.value = ""
            type_input.value = ""
            date_input.value = ""
            harvest_input.value = ""
            health_status_input.value = ""
            location_input.value = ""
            water_input.value = ""
            log_input.value = ""
            user_data = page.data.get("user_data")  # Retrieve stored user_data
            await user_view(page, user_data)
            #page.go("/user")  # Navigate back after saving

        page.update()

    add_plant_layout = ft.Column(
        [
            ft.Text("Add a New Plant", size=24, weight=ft.FontWeight.BOLD),
            name_input, type_input, date_input, harvest_input,
            health_status_input, location_input, water_input, log_input,
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=lambda e: asyncio.create_task(save_info(e))),
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            result_text
        ],
        tight=True
    )

    add_plant_page = ft.View(
        "/add_plant",
        controls=[add_plant_layout]
    )
    page.views.append(add_plant_page)
    page.update()
