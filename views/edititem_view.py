# views/edit_item_view.py
# DI PA TAPOS
import flet as ft
from controllers.inventory_controller import InventoryController

async def edit_item_view(page: ft.Page, user_data, item_id):
    controller = InventoryController()
    item = controller.get_item_by_id(item_id) # get the item, still not asynch

    if item is None:
        page.add(ft.Text("Item not found!"))
        return

    name_field = ft.TextField(label="Name", value=item.name)
    item_type_dropdown = ft.Dropdown(
        label="Type",
        options=[
            ft.dropdown.Option("tool"),
            ft.dropdown.Option("seed"),
            ft.dropdown.Option("other")
        ],
        value=item.item_type
    )
    quantity_field = ft.TextField(label="Quantity", value=str(item.quantity) if item.quantity is not None else "")
    condition_field = ft.TextField(label="Condition", value=item.condition)

    result_message = ft.Text()

    async def save_changes(e):
        success, msg = await controller.update_item(
            item_id=item_id,  # Use the passed item_id
            name=name_field.value,
            item_type=item_type_dropdown.value,
            quantity=int(quantity_field.value) if quantity_field.value else None,
            condition=condition_field.value,
            updated_by=user_data['username']
        )

        if success:
            result_message.value = "Changes saved!"
            result_message.color = ft.colors.GREEN
        else:
            result_message.value = f"Error: {msg}"
            result_message.color=ft.colors.RED

        await page.update_async() # update the UI


    content = ft.Column(
        [
            ft.Text("Edit Item", size=30,weight=ft.FontWeight.BOLD), # added title
            name_field,
            item_type_dropdown,
            quantity_field,
            condition_field,
            ft.Row([
                ft.ElevatedButton("Save", on_click=save_changes),
                ft.ElevatedButton("Back", on_click=lambda e: page.go("/user"))
            ]),
            result_message,  # Display messages here
        ],
        expand=True
    )
    return content

