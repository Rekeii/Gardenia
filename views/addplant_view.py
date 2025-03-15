import flet as ft
from controllers.plant_controller import PlantController
from models.plant_model import PlantType, PlantHealth
import asyncio

async def addplant_view(page: ft.Page):
    print("Navigated to Add Plant Page")  # for debugging
    plant_controller = PlantController()

    name_input = ft.TextField(label="Plant Name")
    type_input = ft.Dropdown(
        label="Plant Type",
        options=[
            ft.dropdown.Option(PlantType.Fruit.value),
            ft.dropdown.Option(PlantType.Vegetable.value),
            ft.dropdown.Option(PlantType.Flower.value),
            ft.dropdown.Option(PlantType.Herb.value),
            ft.dropdown.Option(PlantType.Other.value)
        ]
    )
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
            "observations": []
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
        page.update()

    # Define async handler for the Save button
    async def handle_save(e):
        await save_info(e)

    add_plant_layout = ft.Column(
        [
            ft.Text("Add a New Plant", size=24, weight=ft.FontWeight.BOLD),
            name_input, type_input, date_input, harvest_input,
            health_status_input, location_input, water_input,
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=handle_save),
                    ft.ElevatedButton("Cancel", on_click=lambda e: page.go("/user")),
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            result_text
        ],
        tight=True
    )

    
    page.views.append(
        ft.View(
            "/add_plant",
            controls=[add_plant_layout],
            appbar=ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: page.go("/user")
                ),
                title=ft.Text("Add Plant"),
                center_title=True,
            ),
            scroll=ft.ScrollMode.HIDDEN,
        )
    )
    page.update()
