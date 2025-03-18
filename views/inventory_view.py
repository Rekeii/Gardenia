#inventory_view
import flet as ft
from controllers.inventory_controller import InventoryController
from datetime import datetime
from views.additem_view import additem_view  
import asyncio
from models.inventory_model import InventoryModel  # Add this import if needed

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
                        ft.IconButton(
                            ft.icons.DELETE,
                            on_click=lambda e, id=item._id: delete_item(e, str(id))
                        )
                    ]))
                ]
            ) for item in items
        ]
        page.update()

    def edit_item(e, item_id: str):
        item = controller.get_item_by_id(item_id)
        if item is None:
            message_text.value = "Error: Item not found."
            page.update()
            return

        # Create dialog for editing
        edit_dialog = ft.AlertDialog(
            title=ft.Text("Edit Item"),
            content=ft.Column([
                ft.TextField(label="Name", value=item.name, autofocus=True),
                ft.Dropdown(
                    label="Type",
                    options=[ft.dropdown.Option(t) for t in ["tool", "seed", "other"]],
                    value=item.item_type
                ),
                ft.TextField(label="Quantity", value=str(item.quantity) if item.quantity else ""),
                ft.TextField(label="Condition", value=item.condition if item.condition else ""),
            ], tight=True),
        )

        def save_changes(e):
            try:
                quantity = int(edit_dialog.content.controls[2].value) if edit_dialog.content.controls[2].value.strip() else None
                
                success, msg = controller.update_item(
                    item_id=item_id,
                    name=edit_dialog.content.controls[0].value,
                    item_type=edit_dialog.content.controls[1].value,
                    quantity=quantity,
                    condition=edit_dialog.content.controls[3].value,
                    updated_by=user_data['username']
                )
                
                if success:
                    message_text.value = "Item updated successfully!"
                    refresh_data()  # Refresh the table
                    page.dialog = None
                else:
                    message_text.value = f"Error: {msg}"
                
            except ValueError:
                message_text.value = "Invalid quantity value"
            
            page.update()

        edit_dialog.actions = [
            ft.TextButton("Cancel", on_click=lambda _: close_dialog()),
            ft.TextButton("Save", on_click=save_changes),
        ]

        def close_dialog():
            page.dialog = None
            page.update()

        page.dialog = edit_dialog
        page.update()

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
