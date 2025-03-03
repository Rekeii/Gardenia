from datetime import datetime
from enum import Enum
from typing import Optional, Dict
from bson import ObjectId

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
                 observations: Optional[list] = None,
                 _id: Optional[ObjectId] = None):
        self.name = name
        self.plant_type = plant_type
        self.planting_date = planting_date
        self.estimated_harvest_date = estimated_harvest_date
        self.location = location
        self.health_status = health_status
        self.last_watered = last_watered or datetime.now()
        self.observations = observations or []
        self.created_at = datetime.now()
        self._id = _id

    def to_dict(self) -> Dict:
        data = {
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
        if self._id:
            data['_id'] = self._id
        return data

    @classmethod
    def from_dict(cls, data: Dict):
        def parse_mongo_date(date_data):
            """Helper function to parse MongoDB Extended JSON dates. Since
               Python and MongoDB JSON Date format don't work together"""
            if isinstance(date_data, dict) and '$date' in date_data:
                if isinstance(date_data['$date'], dict) and '$numberLong' in date_data['$date']:
                    # Convert milliseconds to seconds
                    timestamp = int(date_data['$date']['$numberLong']) / 1000.0
                    return datetime.fromtimestamp(timestamp)
                elif isinstance(date_data['$date'], str): #Added str type check case
                     return datetime.fromisoformat(date_data['$date'])
            return date_data  # Return as-is if not a special Mongo date

        return PlantModel(
            name=data.get('name', 'Unknown Plant'),
            plant_type=PlantType(data.get('plant_type', 'other')),
            planting_date=parse_mongo_date(data.get('planting_date', datetime.now())),  # Parse
            estimated_harvest_date=parse_mongo_date(data.get('estimated_harvest_date', datetime.now())),  # Parse
            location=data.get('location', 'Unknown Location'),
            health_status=PlantHealth(data.get('health_status', 'healthy')),
            last_watered=parse_mongo_date(data.get('last_watered', datetime.now())),  # Parse
            observations=data.get('observations', []),
            _id=data.get('_id')
        )
