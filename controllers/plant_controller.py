from models.plant_model import PlantModel, PlantType, PlantHealth
from models.mongodb_client import MongoDBClient
import os

class PlantController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.plants_collection = self.mongodb_client.get_plants_collection()

    async def add_plant(self, plant_model: PlantModel) -> tuple[bool, str]:
        try:
            plant_dict = plant_model.to_dict()
            result = await self.plants_collection.insert_one(plant_dict)
            return True, f"Plant '{plant_model.name}' added successfully."
        except Exception as e:
            return False, str(e)

    async def update_plant_health(self, plant_id: str, new_health_status: PlantHealth) -> tuple[bool, str]:
        try:
            result = await self.plants_collection.update_one(
                {'_id': plant_id},
                {'$set': {'health_status': new_health_status.value}}
            )
            if result.modified_count == 1:
                return True, f"Plant health updated to '{new_health_status.value}'"
            return False, "Plant health not updated."
        except Exception as e:
            return False, str(e)

    async def log_observation(self, plant_id: str, observation: str) -> tuple[bool, str]:
        try:
            result = await self.plants_collection.update_one(
                {'_id': plant_id},
                {'$push': {'observations': observation}}
            )
            if result.modified_count == 1:
                return True, "Observation logged successfully."
            return False, "Observation not logged."
        except Exception as e:
            return False, str(e)

    async def get_plants(self) -> list[PlantModel]:
        try:
            plants = []
            cursor = self.plants_collection.find()
            async for plant in cursor:
                plants.append(PlantModel.from_dict(plant))
            return plants
        except Exception as e:
            print(f"Error fetching plants: {e}")
            return []

    async def get_plant_by_id(self, plant_id: str) -> Optional[PlantModel]:
        try:
            plant = await self.plants_collection.find_one({'_id': plant_id})
            if plant:
                return PlantModel.from_dict(plant)
            return None
        except Exception as e:
            print(f"Error fetching plant by ID: {e}")
            return None

    async def close_connection(self) -> None:
        self.mongodb_client.close_connection()
