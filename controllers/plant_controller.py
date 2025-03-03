from models.plant_model import PlantModel, PlantType, PlantHealth
from models.mongodb_client import MongoDBClient
from bson import ObjectId
import os
from typing import Optional
import asyncio  # New addition: Importing asyncio

class PlantController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.plants_collection = self.mongodb_client.plants_collection

    async def add_plant(self, plant_model: PlantModel) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            plant_dict = plant_model.to_dict()
            # Use run_in_executor for synchronous calls
            result = await loop.run_in_executor(None, self.plants_collection.insert_one, plant_dict)
            return True, f"Plant '{plant_model.name}' added successfully. ID: {result.inserted_id}"
        except Exception as e:
            return False, str(e)

    async def update_plant_health(self, plant_id: str, new_health_status: PlantHealth) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            # Use run_in_executor
            result = await loop.run_in_executor(
                None,
                self.plants_collection.update_one,
                {'_id': ObjectId(plant_id)},
                {'$set': {'health_status': new_health_status.value}}
            )
            if result.modified_count == 1:
                return True, f"Plant health updated to '{new_health_status.value}'"
            else:
                return False, "Plant not found or health not updated."
        except Exception as e:
            return False, str(e)

    async def log_observation(self, plant_id: str, observation: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            # Use run_in_executor
            result = await loop.run_in_executor(
                None,
                self.plants_collection.update_one,
                {'_id': ObjectId(plant_id)},
                {'$push': {'observations': observation}}
            )
            if result.modified_count == 1:
                return True, "Observation logged successfully."
            else:
                return False, "Plant not found or observation not logged."
        except Exception as e:
            return False, str(e)

    async def get_plants(self) -> list[PlantModel]:
        loop = asyncio.get_running_loop()  # Get the current event loop
        try:
            plants = []
            # Use run_in_executor to run the find() operation in a thread
            cursor = await loop.run_in_executor(None, self.plants_collection.find)
             # Iterate over the cursor synchronously
            for plant_data in cursor:
                plants.append(PlantModel.from_dict(plant_data))
            return plants
        except Exception as e:
            print(f"Error fetching plants: {e}")
            return []
    async def get_plant_by_id(self, plant_id: str) -> Optional[PlantModel]:
        loop = asyncio.get_running_loop()
        try:
           plant = await loop.run_in_executor(None, self.plants_collection.find_one, {'_id': ObjectId(plant_id)})
           if plant:
               return PlantModel.from_dict(plant)
           return None
        except Exception as e:
           print(f"Error fetching plants by ID: {e}")

    async def close_connection(self) -> None: # make close_connection also async
        loop = asyncio.get_running_loop()
        # Use run_in_executor because close() is synchronous
        await loop.run_in_executor(None, self.mongodb_client.close_connection)
