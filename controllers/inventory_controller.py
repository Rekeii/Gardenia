from models.inventory_model import InventoryItem
from models.mongodb_client import MongoDBClient
import asyncio
from bson import ObjectId
from typing import List, Optional

class InventoryController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.inventory_collection = self.mongodb_client.inventory_collection  # TO-DO: Reformat documents in Inventory

    async def add_item(self, item_name: str, quantity: int, supplier: Optional[str] = None, last_restocked: Optional[str] = None) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            item = InventoryItem(item_name=item_name, quantity=quantity, supplier=supplier, last_restocked=last_restocked)
            item_dict = item.to_dict()
            result = await loop.run_in_executor(None, self.inventory_collection.insert_one, item_dict)
            return True, f"Item '{item_name}' added. ID: {result.inserted_id}"
        except Exception as e:
            return False, str(e)

    async def get_item(self, item_id: str) -> Optional[InventoryItem]:
        loop = asyncio.get_running_loop()
        try:
            item_data = await loop.run_in_executor(None, self.inventory_collection.find_one, {'_id': ObjectId(item_id)})
            if item_data:
                return InventoryItem.from_dict(item_data)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    async def get_all_items(self) -> List[InventoryItem]:
        loop = asyncio.get_running_loop()
        try:
            items = []
            # Use run_in_executor
            cursor = await loop.run_in_executor(None, self.inventory_collection.find)
            for item_data in cursor:
                items.append(InventoryItem.from_dict(item_data))
            return items
        except Exception as e:
            print(f"Error: {e}")
            return []

    async def update_quantity(self, item_id: str, new_quantity: int) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(
                None,
                self.inventory_collection.update_one,
                {'_id': ObjectId(item_id)},
                {'$set': {'quantity': new_quantity}}
            )
            if result.modified_count == 1:
                return True, "Quantity updated."
            return False, "Item not found or update failed."
        except Exception as e:
            return False, str(e)
    async def close_connection(self) -> None: # make close_connection also async
        loop = asyncio.get_running_loop()
        # Use run_in_executor because close() is synchronous
        await loop.run_in_executor(None, self.mongodb_client.close_connection)

