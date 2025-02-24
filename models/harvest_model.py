from datetime import datetime
from typing import Dict, Optional

class HarvestModel:
    def __init__(self,
                 plant_id: str,
                 harvest_date: datetime,
                 quantity: int,
                 distribution_date: Optional[datetime] = None,
                 distribution_status: str = "pending"):
        self.plant_id = plant_id
        self.harvest_date = harvest_date
        self.quantity = quantity
        self.distribution_date = distribution_date
        self.distribution_status = distribution_status
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "plant_id": self.plant_id,
            "harvest_date": self.harvest_date.isoformat(),
            "quantity": self.quantity,
            "distribution_date": self.distribution_date.isoformat() if self.distribution_date else None,
            "distribution_status": self.distribution_status,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return HarvestModel(
            plant_id=data['plant_id'],
            harvest_date=datetime.fromisoformat(data['harvest_date']),
            quantity=data['quantity'],
            distribution_date=datetime.fromisoformat(data['distribution_date']) if data.get('distribution_date') else None,
            distribution_status=data.get('distribution_status', "pending")
        )
