from typing import Optional, Dict
from bson import ObjectId

class InventoryItem:
    def __init__(self, item_name: str, quantity: int,
                 supplier: Optional[str] = None, last_restocked: Optional[str] = None, _id: Optional[ObjectId]=None):
        self.item_name = item_name
        self.quantity = quantity
        self.supplier = supplier
        self.last_restocked = last_restocked
        self._id = _id;

    def to_dict(self) -> Dict:
        data = {
            "item_name": self.item_name,
            "quantity": self.quantity,
            "supplier": self.supplier,
            "last_restocked": self.last_restocked
        }
        if self._id:
            data['_id'] = self._id
        return data
    @classmethod
    def from_dict(cls, data:Dict):
        return InventoryItem(
            item_name = data.get('item_name', 'Unknown Item'),
            quantity = data.get('quantity', 0),
            supplier = data.get('supplier'),
            last_restocked = data.get('last_restocked'),
            _id = data.get('_id')
        )

