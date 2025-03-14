#inventory_view
import flet as ft
from controllers.inventory_controller import InventoryController
from datetime import datetime
from views.additem_view import additem_view  
import asyncio

async def inventory_view(page: ft.Page, user_data):
    controller = InventoryController()
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Type")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Condition")),
            ft.DataColumn(ft.Text("Updated By")),
            ft.DataColumn(ft.Text("Last Updated")),
            ft.DataColumn(ft.Text("Actions"))
        ],
        expand=True
    )

    message_text = ft.Text("")

    def refresh_data():
        items = controller.get_all_items()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item.name or "-")),
                    ft.DataCell(ft.Text(item.item_type or "-")),  
                    ft.DataCell(ft.Text(str(item.quantity) if item.quantity is not None else "-")),
                    ft.DataCell(ft.Text(item.condition or "-")),
                    ft.DataCell(ft.Text(item.updated_by or "-")),
                    ft.DataCell(ft.Text(item.last_updated.strftime("%Y-%m-%d %H:%M") if item.last_updated else "-")),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, id=item._id: edit_item(e, str(id))),
                        ft.IconButton(ft.icons.DELETE,on_click=lambda e, id=item._id: delete_item(e, str(id)))
                    ]))
                ]
            ) for item in items
        ]
        page.update()

    async def edit_item(e, item_id):
        item = controller.get_item_by_id(item_id)
        if item is None:
            message_text.value = "Error: Item not found."
            page.update()
            return

        # Store original values *before* creating controls
        original_name = item.name
        original_type = item.item_type
        original_quantity = item.quantity
        original_condition = item.condition

        edit_name = ft.TextField(label="Name", value=original_name)
        edit_type = ft.Dropdown(
            label="Type",
            options=[ft.dropdown.Option(t) for t in ["tool", "seed", "other"]],
            value=original_type
        )
        edit_quantity = ft.TextField(label="Quantity", value=str(original_quantity) if original_quantity is not None else "")
        edit_condition = ft.TextField(label="Condition", value=original_condition)

        async def save_changes(e):
            # Remove 'await' for update_item
            success, msg = controller.update_item(
                item_id=item_id,
                name=edit_name.value,
                item_type=edit_type.value,
                quantity=int(edit_quantity.value) if edit_quantity.value else None,
                condition=edit_condition.value,
                updated_by=user_data['username']
            )
            if success:
                message_text.value = "Changes saved!"
                refresh_data()
            else:
                message_text.value = f"Error: {msg}"
            set_editing_mode(False)
            page.update()

        async def cancel_changes(e):
            set_editing_mode(False)
            page.update()
        
        save_button = ft.ElevatedButton("Save", on_click=save_changes)
        cancel_button = ft.TextButton("Cancel", on_click=cancel_changes)

        controls =  [
                ft.Text("Edit Item", size=18, weight=ft.FontWeight.BOLD), edit_name,
                edit_type, edit_quantity, edit_condition,
                save_button, cancel_button, message_text
            ]

        def set_editing_mode(editing: bool):
            if editing:
                for control in controls:
                    inventory_view_column.controls.append(control)
            else:
                for control in controls:
                    if control in inventory_view_column.controls:
                        inventory_view_column.controls.remove(control)
            page.update()

        set_editing_mode(True)

    def delete_item(e, item_id):
        success, msg = controller.delete_item(item_id)
        if success:
            message_text.value = "Item deleted"
            refresh_data()  # Refresh the table after deletion
        else:
            message_text.value = f"Error: {msg}"
        page.update()

    async def go_to_add_item(e):
        page.route = "/add_item"
        # Generate the add item view
        add_view = await additem_view(page, user_data)
        # Clear existing views and append the new one
        page.views.clear()
        page.views.append(add_view)
        # Update the page
        await page.update()

    inventory_view_column = ft.Column([
        ft.ElevatedButton("Add Item", on_click=go_to_add_item),
        table,
        message_text,
    ], expand=True)

    refresh_data()

    return inventory_view_column
