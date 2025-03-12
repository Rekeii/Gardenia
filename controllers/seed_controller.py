from seed_class import SeedModel
from models.mongodb_client import MongoDBClient
import asyncio
from bson import ObjectId
from typing import List, Optional

class SeedServiceController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.seed_collection = self.mongodb_client.seed_collection

    async def add_seed(self, name: str, quantity: int) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            seed = SeedModel(name=name, quantity=quantity)
            seed_dict = seed.to_dict()
            result = await loop.run_in_executor(None, self.seed_collection.insert_one, seed_dict)
            return True, f"Seed '{name}' added. ID: {result.inserted_id}"
        except Exception as e:
            return False, str(e)

    async def plant_seed(self, seed_id: str, quantity: int) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            seed_data = await loop.run_in_executor(None, self.seed_collection.find_one, {'_id': ObjectId(seed_id)})
            if not seed_data:
                return False, "Seed not found."
            
            seed = SeedModel.from_dict(seed_data)
            if seed.quantity < quantity:
                return False, "Not enough seeds available."

            new_quantity = seed.quantity - quantity
            result = await loop.run_in_executor(
                None,
                self.seed_collection.update_one,
                {'_id': ObjectId(seed_id)},
                {'$set': {'quantity': new_quantity}}
            )
            if result.modified_count == 1:
                return True, "Seed planted."
            return False, "Failed to update seed quantity."
        except Exception as e:
            return False, str(e)

    async def update_seed_quantity(self, seed_id: str, new_quantity: int) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(
                None,
                self.seed_collection.update_one,
                {'_id': ObjectId(seed_id)},
                {'$set': {'quantity': new_quantity}}
            )
            if result.modified_count == 1:
                return True, "Seed quantity updated."
            return False, "Seed not found or update failed."
        except Exception as e:
            return False, str(e)

    async def get_all_seeds(self) -> List[SeedModel]:
        loop = asyncio.get_running_loop()
        try:
            cursor = await loop.run_in_executor(None, self.seed_collection.find)
            return [SeedModel.from_dict(seed) for seed in cursor]
        except Exception as e:
            print(f"Error: {e}")
            return []

    async def remove_seed(self, seed_id: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(None, self.seed_collection.delete_one, {'_id': ObjectId(seed_id)})
            if result.deleted_count == 1:
                return True, "Seed removed."
            return False, "Seed not found."
        except Exception as e:
            return False, str(e)
