from datetime import datetime
from enum import Enum
from typing import Optional, Dict

class PlantType(str, Enum):
    Fruit = "fruit"
    Vegetable = "vegetable"
    Flower = "flower"
    Herb = "herb"
    Other = "other"

class PlantHealth(str, Enum):
    Healthy = "healthy"
    NeedsWater = "needs_water"
    PestsDetected = "pests_detected"
    ReadyForHarvest = "ready_for_harvest"

class PlantModel:
    def __init__(self, 
                 name: str,
                 plant_type: PlantType,
                 planting_date: datetime,
                 estimated_harvest_date: datetime,
                 location: str,
                 health_status: PlantHealth,
                 last_watered: Optional[datetime] = None,
                 observations: Optional[list] = None):
        self.name = name
        self.plant_type = plant_type
        self.planting_date = planting_date
        self.estimated_harvest_date = estimated_harvest_date
        self.location = location
        self.health_status = health_status
        self.last_watered = last_watered or datetime.now()
        self.observations = observations or []
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "plant_type": self.plant_type.value,
            "planting_date": self.planting_date.isoformat(),
            "estimated_harvest_date": self.estimated_harvest_date.isoformat(),
            "location": self.location,
            "health_status": self.health_status.value,
            "last_watered": self.last_watered.isoformat(),
            "observations": self.observations,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return PlantModel(
            name=data['name'],
            plant_type=PlantType(data['plant_type']),
            planting_date=datetime.fromisoformat(data['planting_date']),
            estimated_harvest_date=datetime.fromisoformat(data['estimated_harvest_date']),
            location=data['location'],
            health_status=PlantHealth(data['health_status']),
            last_watered=datetime.fromisoformat(data['last_watered'])
        )
