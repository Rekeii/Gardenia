import flet as ft
from controllers.plant_controller import PlantController
import asyncio
from datetime import datetime

async def plant_log_view(page: ft.Page, plant_id: str):
    plant_controller = PlantController()
    plant = await plant_controller.get_plant_by_id(plant_id)

    if not plant:
        page.add(ft.Text("Plant not found.", style=ft.TextThemeStyle.HEADLINE_MEDIUM))
        return

    log_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Date", style=ft.TextThemeStyle.TITLE_MEDIUM)),
            ft.DataColumn(ft.Text("Observation", style=ft.TextThemeStyle.TITLE_MEDIUM)),
        ],
        rows=[],
        heading_row_color=ft.colors.BLUE_GREY_100,
        border=ft.border.all(1, ft.colors.GREY_400)
    )

    # Populate the table with existing log entries
    for observation in plant.observations:
        try:
            # Attempt 19-character timestamp approach
            date_str = observation[:19].strip()
            obs_text = observation[20:].strip()
            obs_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, IndexError):
            # Fallback to splitting on the first colon
            try:
                parts = observation.split(":", 1)
                if len(parts) == 2:
                    date_str = parts[0].strip()
                    obs_text = parts[1].strip()
                    obs_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                else:
                    obs_date = None
                    obs_text = observation
            except ValueError:
                obs_date = None
                obs_text = observation

        log_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(obs_date.strftime('%Y-%m-%d %H:%M:%S') if obs_date else "Invalid Date")),
                    ft.DataCell(ft.Text(obs_text)),
                ]
            )
        )

    new_log_entry = ft.TextField(
        label="Enter your observation here",
        hint_text="e.g., 'Added compost', 'Watered plant'",
        min_lines=1,
        max_lines=3,
        expand=True,
        border_radius=5,
        filled=True,
        content_padding=ft.padding.symmetric(10, 15),
    )

    result_text = ft.Text(value="", size=14)

    async def add_log_entry(e):
        if not new_log_entry.value.strip():
            result_text.value = "Please enter a valid observation."
            result_text.color = ft.colors.RED
            page.update()
            return

        observation_str = f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}: {new_log_entry.value}"
        success, message = await plant_controller.log_observation(plant_id, observation_str)
        
        # Clear input and show result
        new_log_entry.value = ""
        result_text.value = message
        result_text.color = ft.colors.GREEN if success else ft.colors.RED

        if success:
            # Reload data
            nonlocal plant, log_table
            plant = await plant_controller.get_plant_by_id(plant_id)
            log_table.rows.clear()
            
            # Repopulate table with new data
            for observation in plant.observations:
                try:
                    date_str = observation[:19].strip()
                    obs_text = observation[20:].strip()
                    obs_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                except:
                    obs_date = None
                    obs_text = observation

                log_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(obs_date.strftime('%Y-%m-%d %H:%M:%S') if obs_date else "Invalid Date")),
                            ft.DataCell(ft.Text(obs_text)),
                        ]
                    )
                )

        page.update()

    async def go_back_to_user_view(e):
        if len(page.views) > 1:
            page.views.pop()
            if 'user_data' in page.data:
                from views.user_view import user_view
                await user_view(page, page.data['user_data'])
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
        
        
    # Improved UI Layout
    log_view_layout = ft.Container(
        ft.Column(
            [
                ft.Text(f"Plant Log for {plant.name}", 
                        style=ft.TextThemeStyle.HEADLINE_LARGE,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                
                ft.Container(
                    log_table,
                    margin=ft.margin.only(bottom=20),
                    width=800,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(10, 20)
                ),
                
                ft.Container(
                    ft.Row(
                        [
                            new_log_entry,
                            ft.ElevatedButton(
                                "Add Observation",
                                on_click=add_log_entry,
                                style=ft.ButtonStyle(
                                    color={ft.ControlState.HOVERED: ft.colors.GREEN_ACCENT}
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    margin=ft.margin.only(bottom=20)
                ),
                
                ft.Container(
                    result_text,
                    margin=ft.margin.only(top=20),
                    padding=ft.padding.symmetric(8, 16),
                    bgcolor=lambda: ft.colors.GREEN_100 if result_text.color == ft.colors.GREEN else ft.colors.RED_100,
                    border_radius=5
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            scroll=ft.ScrollMode.AUTO  # Enable scrolling
        ),
        padding=ft.padding.symmetric(40, 60),
        width=1200,
        alignment=ft.alignment.center,
        height=page.window_height * 0.9  # Set fixed height for scrolling
    )

    # Final View setup
    plant_log_page = ft.View(
        "/plant_log",
        controls=[log_view_layout],
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

    # Push the new view and update
    page.views.append(plant_log_page)
    page.update()