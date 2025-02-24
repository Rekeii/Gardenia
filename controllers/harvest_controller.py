from models.harvest_model import HarvestModel
from models.plant_model import PlantModel, PlantHealth
from models.mongodb_client import MongoDBClient

class HarvestController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.plants_collection = MongoDBClient().get_plants_collection()
        self.harvests_collection = MongoDBClient().get_harvests_collection()

    async def mark_ready_for_harvest(self, plant_id: str) -> tuple[bool, str]:
        try:
            # Update plant health status
            plant_controller = PlantController()
            success, message = await plant_controller.update_plant_health(plant_id, PlantHealth.ReadyForHarvest)
            if not success:
                return False, message

            # Create harvest record
            plant = await plant_controller.get_plant_by_id(plant_id)
            if not plant:
                return False, "Plant not found."

            harvest = HarvestModel(
                plant_id=plant_id,
                harvest_date=datetime.now(),
                quantity=1
            )
            result = await self.harvests_collection.insert_one(harvest.to_dict())
            if result.inserted_id:
                return True, f"Plant '{plant.name}' marked ready for harvest."
            return False, "Failed to create harvest record."

        except Exception as e:
            return False, str(e)

    async def distribute_harvest(self, plant_id: str) -> tuple[bool, str]:
        try:
            # Update harvest record
            harvest = await self.harvests_collection.find_one({'plant_id': plant_id, 'distribution_status': 'pending'})
            if not harvest:
                return False, "No pending harvest found for this plant."

            updated_harvest = HarvestModel.from_dict(harvest)
            updated_harvest.distribution_date = datetime.now()
            updated_harvest.distribution_status = "distributed"

            result = await self.harvests_collection.update_one(
                {'_id': harvest['_id']},
                {'$set': updated_harvest.to_dict()}
            )

            if result.modified_count == 1:
                return True, "Harvest distributed successfully."
            return False, "Failed to update harvest status."
        except Exception as e:
            return False, str(e)

    async def get_ready_for_harvest_plants(self) -> list[PlantModel]:
        try:
            plants = await self.plants_collection.find({'health_status': PlantHealth.ReadyForHarvest})
            plant_list = []
            async for plant in plants:
                plant_list.append(PlantModel.from_dict(plant))
            return plant_list
        except Exception as e:
            print(f"Error fetching ready for harvest plants: {e}")
            return []

    async def get_all_harvests(self) -> list[HarvestModel]:
        try:
            harvests = []
            cursor = self.harvests_collection.find()
            async for harvest in cursor:
                harvests.append(HarvestModel.from_dict(harvest))
            return harvests
        except Exception as e:
            print(f"Error fetching harvests: {e}")
            return []

    async def close_connection(self) -> None:
        self.mongodb_client.close_connection()
