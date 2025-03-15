import flet as ft
from controllers.plant_controller import PlantController
import asyncio
from models.plant_model import PlantType, PlantHealth

async def addplant_view(page: ft.Page):
    print("Navigated to Add Plant Page")

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
    ) #dropdown menu for enums suggested
    date_input = ft.TextField(label="Planting Date (MM/DD/YYYY)")
    harvest_input = ft.TextField(label="Harvest Date (MM/DD/YYYY)")
    # status_input = ft.TextField(label="Status") #Status Removed
    health_status_input = ft.Dropdown(
        label="Health Status",
        options=[
            ft.dropdown.Option(PlantHealth.Healthy.value),
            ft.dropdown.Option(PlantHealth.NeedsWater.value),
            ft.dropdown.Option(PlantHealth.PestsDetected.value),
            ft.dropdown.Option(PlantHealth.ReadyForHarvest.value)
    
        ]
    ) #dropdown menu for enums suggested
    location_input = ft.TextField(label = "Location") #Added
    water_input = ft.TextField(label="Last Date of Watering (MM/DD/YYYY)")
    log_input = ft.TextField(label="Plant Log Entry")

    result_text = ft.Text("")
    async def save_info(e):
        # Create the dictionary *here* to pass to the controller.
        new_plant = {
            "name": name_input.value,
            "plant_type": type_input.value,  # Pass the string value
            "planting_date": date_input.value,
            "estimated_harvest_date": harvest_input.value,
           # "status": status_input.value, #Status removed
            "health_status": health_status_input.value,  # Get selected value
            "location" : location_input.value,  # Get Value
            "last_watered": water_input.value,
            "observations": log_input.value
        }


        success, message = await plant_controller.add_plant(new_plant)  # Pass the dict
        result_text.value = message  # Display success/error message
        if success:
           name_input.value = ""
           type_input.value =""
           date_input.value =""
           harvest_input.value =""
           health_status_input.value =""
           location_input.value=""
           water_input.value =""
           log_input.value =""
        page.update()

    # Layout
    add_plant_layout = ft.Column(
        [
            ft.Text("Add a New Plant", size=24, weight=ft.FontWeight.BOLD),
            name_input, type_input, date_input, harvest_input, health_status_input, location_input, water_input, log_input, #added health and location
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

    async def go_back_to_user_view(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()  # Force UI update
            return

        # Fallback to manual navigation
        if 'user_data' in page.data:
            from views.user_view import user_view
            await user_view(page, page.data['user_data'])
            page.views.pop()  # Remove current view
            page.update()
        else:
            print("Error: User data not found, cannot navigate back.")

    # Create the View
    add_plant_page = ft.View(
        "/add_plant",
        controls=[add_plant_layout],
        appbar=ft.AppBar(
            leading=ft.IconButton(  # Back button
                icon=ft.icons.ARROW_BACK,
                on_click=go_back_to_user_view,
            ),
            title=ft.Text("Plant Log"),
            center_title=True,
        ),
        scroll=ft.ScrollMode.HIDDEN,
    )

    page.views.append(add_plant_page)
    page.update()
