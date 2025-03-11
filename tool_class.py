from enum import Enum
from typing import Optional, Dict
from bson import ObjectId


class ToolCondition(str, Enum):
    Good = "good"
    NeedsRepair = "needs_repair"

class ToolModel:
    def __init__(self, name: str, 
                 condition:ToolCondition,
                 _id: Optional[ObjectId] = None):
        self.name = name
        self.condition = condition
        self._id = _id

    def repair(self):
        if self.condition == ToolCondition.NeedsRepair:
            self.condition = ToolCondition.Good
    
    def to_dict(self) -> Dict:
        return {
            "_id":self._id,
            "name":self.name,
            "condition": self.condition
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name = data['name'],
            condition = ToolCondition(data["condition"]),
            _id = data.get("_id")
        )
        

        

