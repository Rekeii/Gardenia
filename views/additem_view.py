#additem_view
import flet as ft
from controllers.inventory_controller import InventoryController
from models.tool_model import ToolCondition

async def additem_view(page: ft.Page, user_data):
    controller = InventoryController()

    async def close_view(e):  
        page.go('/') 

    name_field = ft.TextField(label="Item Name")
    type_dropdown = ft.Dropdown(
        label="Item Type",
        options=[
            ft.dropdown.Option("tool"),
            ft.dropdown.Option("seed"),
            ft.dropdown.Option("other")
        ]
    )

    quantity_field = ft.TextField(label="Quantity")
    condition_dropdown = ft.Dropdown(
        label="Condition",
        options=[
            ft.dropdown.Option(ToolCondition.Good.value),
            ft.dropdown.Option(ToolCondition.NeedsRepair.value),
            ft.dropdown.Option("expired"),
            ft.dropdown.Option("available"),
        ]
    )

    result_text = ft.Text("")

    def save_item(e):
        try:
            quantity = int(quantity_field.value) if quantity_field.value else None
            if quantity is not None and quantity < 0:
                result_text.value = "Quantity cannot be negative."
                page.update()
                return

            # Remove 'await' since add_item is now synchronous
            success, msg = controller.add_item(
                name=name_field.value,
                item_type=type_dropdown.value,
                quantity=quantity,
                condition=condition_dropdown.value,
                updated_by=user_data['username']
            )
            if success:
                result_text.value = "Item added successfully!"
                name_field.value = ""
                quantity_field.value = ""
                type_dropdown.value = None
                condition_dropdown.value = None
                
                # Navigate back to inventory view
                page.go('/user')
                
            page.update()
            
        except ValueError:
            result_text.value = "Invalid quantity. Please enter a valid number."
        

    add_item_layout = ft.Column(
        [
            ft.Text("Add New Item", size=24, weight=ft.FontWeight.BOLD),
            name_field, type_dropdown, quantity_field, condition_dropdown,
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_item),
                    #ft.ElevatedButton("Back", on_click=lambda e: page.go('/')) # close view
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            result_text,
        ],
        tight=True
    )

    # Create the AppBar with a back button
    appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: page.go("/user")  # Navigate back to previous view (e.g., inventory)
        ),
        title=ft.Text("Add New Item"),
        center_title=True,
    )

    return ft.View(
        "/add_item",
        controls=[add_item_layout],
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: page.go("/user")  # Single back button
            ),
            title=ft.Text("Add New Item"),
            center_title=True,
        ),
        scroll=ft.ScrollMode.HIDDEN,
    )
    
    
