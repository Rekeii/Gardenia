from datetime import datetime
from bson import ObjectId
from typing import Optional

class InventoryModel:
    def __init__(
        self,
        name: str,
        item_type: str,
        quantity: Optional[int] = None,
        condition: Optional[str] = None,
        last_updated: datetime = datetime.now(),
        updated_by: str = "",
        _id: Optional[ObjectId] = None
    ):
        self.name = name
        self.item_type = item_type
        self.quantity = quantity
        self.condition = condition
        self.last_updated = last_updated
        self.updated_by = updated_by
        self._id = _id

    def to_dict(self) -> dict:
        return {
            "_id": str(self._id) if self._id else None,
            "name": self.name,
            "item_type": self.item_type,
            "quantity": self.quantity,
            "condition": self.condition,
            "last_updated": self.last_updated,
            "updated_by": self.updated_by
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            item_type=data.get("item_type"),
            quantity=data.get("quantity"),
            condition=data.get("condition"),
            last_updated=data.get("last_updated"),
            updated_by=data.get("updated_by"),
            _id=ObjectId(data.get("_id")) if data.get("_id") else None
        )
