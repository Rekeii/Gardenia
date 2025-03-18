#inventory_controller
# controllers/inventory_controller.py
from models.inventory_model import InventoryModel  # Update this import
from models.mongodb_client import MongoDBClient
from bson import ObjectId
from datetime import datetime
from typing import Optional

class InventoryController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.inventory_collection = self.mongodb_client.inventory_collection

    def add_item(self, name: str, item_type: str, quantity=None, condition=None, updated_by="") -> tuple[bool, str]:
        try:
            new_item = InventoryModel(
                name=name,
                item_type=item_type,
                quantity=quantity,
                condition=condition,
                last_updated=datetime.now(),
                updated_by=updated_by
            )
            # Remove 'await' since this is synchronous
            self.inventory_collection.insert_one(new_item.to_dict())
            return True, "Item added successfully"
        except Exception as e:
            return False, str(e)


    def update_item(self, item_id: str, **kwargs) -> tuple[bool, str]:
        try:
            # Build update dictionary with only provided values
            update_data = {"$set": {}}
            
            if "name" in kwargs:
                update_data["$set"]["name"] = kwargs["name"]
            if "item_type" in kwargs:
                update_data["$set"]["item_type"] = kwargs["item_type"]
            if "quantity" in kwargs:
                update_data["$set"]["quantity"] = kwargs["quantity"]
            if "condition" in kwargs:
                update_data["$set"]["condition"] = kwargs["condition"]
            
            # Always update these fields
            update_data["$set"].update({
                "last_updated": datetime.now(),
                "updated_by": kwargs.get("updated_by", "")
            })

            result = self.inventory_collection.update_one(
                {"_id": ObjectId(item_id)},
                update_data
            )

            if result.modified_count > 0:
                return True, "Item updated successfully"
            else:
                return False, "No changes made or item not found"
                
        except Exception as e:
            return False, str(e)

    def get_all_items(self) -> list[InventoryModel]:
        cursor = self.inventory_collection.find()
        items = list(cursor)
        return [InventoryModel.from_dict(item) for item in items]

    def get_item_by_id(self, item_id: str) -> Optional[InventoryModel]:
        try:
            item_data = self.inventory_collection.find_one({"_id": ObjectId(item_id)})
            if item_data:
                return InventoryModel.from_dict(item_data)
            return None
        except Exception as e:
            print(f"Error getting item by ID: {e}")
            return None

    def delete_item(self, item_id: str) -> tuple[bool, str]:
        try:
            result = self.inventory_collection.delete_one({"_id": ObjectId(item_id)})
            if result.deleted_count == 1:
                return True, "Item deleted successfully"
            else:
                return False, "Item not found"
        except Exception as e:
            return False, str(e)
