from enum import Enum
from datetime import datetime
from bson import ObjectId
from typing import Optional

class ItemType(Enum):
    TOOL = "tool"
    SEED = "seed"
    HARVEST = "harvest"
    OTHER = "other"

class InventoryModel:  # Changed from InventoryItem to InventoryModel (Consistent Naming Scheme)
    def __init__(self, 
                 name: str,
                 item_type: str,
                 quantity: Optional[int] = None,
                 condition: Optional[str] = None,
                 plant_source: Optional[str] = None,  # For harvests, store plant name
                 harvest_date: Optional[datetime] = None,  # For harvests
                 updated_by: str = "",
                 last_updated: Optional[datetime] = None,
                 _id: Optional[ObjectId] = None):
        self.name = name
        self.item_type = item_type
        self.quantity = quantity
        self.condition = condition
        self.plant_source = plant_source
        self.harvest_date = harvest_date
        self.updated_by = updated_by
        self.last_updated = last_updated or datetime.now()
        self._id = _id

    def to_dict(self):
        data = {
            "name": self.name,
            "item_type": self.item_type,
            "quantity": self.quantity,
            "condition": self.condition,
            "updated_by": self.updated_by,
            "last_updated": self.last_updated
        }
        if self.plant_source:
            data["plant_source"] = self.plant_source
        if self.harvest_date:
            data["harvest_date"] = self.harvest_date
        if self._id:
            data["_id"] = self._id
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            item_type=data.get("item_type"),
            quantity=data.get("quantity"),
            condition=data.get("condition"),
            plant_source=data.get("plant_source"),
            harvest_date=data.get("harvest_date"),
            updated_by=data.get("updated_by", ""),
            last_updated=data.get("last_updated"),
            _id=data.get("_id")
        )
