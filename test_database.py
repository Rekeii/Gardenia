# test_db.py
from pymongo import MongoClient
import os
from datetime import datetime
from bson import ObjectId
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
                 plant_type: PlantType,  # Changed from "type"
                 planting_date: datetime,
                 estimated_harvest_date: datetime,
                 location: str,
                 health_status: PlantHealth,
                 last_watered: Optional[datetime] = None,
                 observations: Optional[list] = None,
                 _id: Optional[ObjectId] = None):  # Add _id, make it optional
        self.name = name
        self.plant_type = plant_type
        self.planting_date = planting_date
        self.estimated_harvest_date = estimated_harvest_date
        self.location = location
        self.health_status = health_status
        self.last_watered = last_watered or datetime.now()
        self.observations = observations or []
        self.created_at = datetime.now()
        self._id = _id  # Store the ObjectId

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
        if self._id:  # Include _id in the dictionary if it exists
            data['_id'] = self._id
        return data

    @classmethod
    def from_dict(cls, data: Dict):
        def parse_mongo_date(date_data):
            """Helper function to parse MongoDB Extended JSON dates."""
            if isinstance(date_data, dict) and '$date' in date_data:
                if isinstance(date_data['$date'], dict) and '$numberLong' in date_data['$date']:
                    # Convert milliseconds to seconds
                    timestamp = int(date_data['$date']['$numberLong']) / 1000.0
                    return datetime.fromtimestamp(timestamp)
                elif isinstance(date_data['$date'], str):  # Added str type check case
                    return datetime.fromisoformat(date_data['$date'])
            return date_data  # Return as-is if not a special Mongo date

        # Handle potential missing fields gracefully
        return PlantModel(
            name=data.get('name', 'Unknown Plant'),
            plant_type=PlantType(data.get('plant_type', 'other')),  # Handle missing/invalid
            planting_date=parse_mongo_date(data.get('planting_date', datetime.now().isoformat())),
            estimated_harvest_date=parse_mongo_date(data.get('estimated_harvest_date', datetime.now().isoformat())),
            location=data.get('location', 'Unknown Location'),
            health_status=PlantHealth(data.get('health_status', 'healthy')),  # Handle missing
            last_watered=parse_mongo_date(data.get('last_watered', datetime.now().isoformat())),
            observations=data.get('observations', []),
            _id=data.get('_id')  # Get the ObjectId
        )
def test_connection_and_data():
    uri = os.getenv('MONGODB_URI', "mongodb+srv://gardenia_1:106lgardenia@cluster0.pmlml.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client = MongoClient(uri)
    db = client['gardenia']
    plants_collection = db['plants']

    try:
        # Fetch all documents from the 'plants' collection
        cursor = plants_collection.find()
        plants = []
        for plant_data in cursor:
            plants.append(PlantModel.from_dict(plant_data))


        # Print the data for verification
        if plants:
            for plant in plants:
                print(f"Plant Name: {plant.name}")
                print(f"  Type: {plant.plant_type}")
                print(f"  Planting Date: {plant.planting_date}")
                print(f"  Estimated Harvest Date: {plant.estimated_harvest_date}")
                print(f"  Health Status: {plant.health_status}")
                print(f"  Last Watered: {plant.last_watered}")
                print(f"  Observations: {plant.observations}")
                print(f"  Location: {plant.location}")
                print(f"  _id: {plant._id}")  # Print the _id
                print("-" * 20)
        else:
            print("No plants found in the collection.")

        # Verify connection by getting the server info
        server_info = client.server_info()
        print(f"Successfully connected to MongoDB server. Version: {server_info['version']}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    test_connection_and_data()

