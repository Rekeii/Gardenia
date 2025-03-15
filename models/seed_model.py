from typing import Optional,Dict
from bson import ObjectId

class SeedModel:
    def __init__(self, name:str,
                 quantity: int,
                 _id:Optional[ObjectId] = None):
        self.name = name
        self.quantity = quantity
        self._id = _id

    def plant(self, quantity: int):
        if quantity <= self.quantity:
            self.quantity -= quantity

    def to_dict(self) -> Dict:
        return {
            "_id": self._id,
            "name":self.name,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name = data['name'],
            quantity = data['quantity'],
            _id = ObjectId(data.get("_id")) if data.get("_id") else None # added object id

        )
