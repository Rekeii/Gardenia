from models.plant_model import PlantModel, PlantType, PlantHealth
from models.mongodb_client import MongoDBClient
from bson import ObjectId
import os
from typing import Optional
from datetime import datetime 
import asyncio
from controllers.volunteer_controller import VolunteerController

class PlantController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.plants_collection = self.mongodb_client.plants_collection

    async def add_plant(self, plant_data: dict) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()

        try:
            try:
                planting_date = datetime.strptime(plant_data['planting_date'], '%m/%d/%Y')
                estimated_harvest_date = datetime.strptime(plant_data['estimated_harvest_date'], '%m/%d/%Y')
                last_watered = datetime.strptime(plant_data['last_watered'], '%m/%d/%Y')
            except ValueError as e:
                return False, f"Invalid date format: {e}.  Please use MM/DD/YYYY."
            except KeyError as e:
                return False, f"Missing required field: {e}"
            
            try:
                plant_type_enum = PlantType(plant_data['plant_type'])
                health_status_enum = PlantHealth(plant_data.get('health_status', 'healthy'))
                
            except ValueError as e:
                 return False, f"Incorrect Plant Type or Health Status Input: {e}"

            plant_model = PlantModel(
                name=plant_data['name'],
                plant_type=plant_type_enum,
                planting_date=planting_date,
                estimated_harvest_date=estimated_harvest_date,
                location=plant_data.get('location', 'Unknown'),
                health_status=health_status_enum,
                last_watered=last_watered,
                observations=[plant_data['observations']] if plant_data['observations'] else [],
                _id=None
            )

            plant_dict = plant_model.to_dict()
            plant_dict["planting_date"] = planting_date
            plant_dict["estimated_harvest_date"] = estimated_harvest_date
            plant_dict["last_watered"] = last_watered
            print(plant_dict)

        except Exception as e:
            return False, f"Data validation error: {e}"

        try:
            result = await loop.run_in_executor(None, self.plants_collection.insert_one, plant_dict)
            return True, f"Plant '{plant_data['name']}' added successfully. ID: {result.inserted_id}"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    async def update_plant_health(self, plant_id: str, new_status: PlantHealth) -> tuple[bool, str]:
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                self.plants_collection.update_one,
                {'_id': ObjectId(plant_id)},
                {'$set': {'health_status': new_status.value}}
            )
            if result.modified_count == 1:
                return True, f"Plant health updated to '{new_status.value}'"
            else:
                return False, "Plant not found or health not updated."
        except Exception as e:
            return False, str(e)

    async def log_observation(self, plant_id: str, observation: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
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
        loop = asyncio.get_running_loop()
        try:
            plants = []
            cursor = await loop.run_in_executor(None, self.plants_collection.find)
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

    async def close_connection(self) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.mongodb_client.close_connection)

    async def check_harvest_dates(self, last_logged_user: str) -> None:
        plants = await self.get_plants()
        volunteer_controller = VolunteerController()
        
        for plant in plants:
            if (plant.estimated_harvest_date 
                and plant.estimated_harvest_date.date() <= datetime.now().date() 
                and plant.health_status != PlantHealth.HARVESTED):
                
                task_name = f"Harvest {plant.name}"
                success, msg = await volunteer_controller.add_task(
                    taskName=task_name,
                    frequency="once",
                    assignedVolunteerId=last_logged_user,
                    plant_id=str(plant._id)
                )
                
                if success:
                    print(f"Created harvest task for {plant.name}")
                else:
                    print(f"Failed to create harvest task: {msg}")
