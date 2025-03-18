from models.seed_model import SeedModel
from models.mongodb_client import MongoDBClient
from bson import ObjectId
from typing import List, Optional
import asyncio, datetime

class SeedServiceController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.inventory_collection = self.mongodb_client.inventory_collection

    async def add_seed(self, name: str, quantity: int, updated_by: str) -> tuple[bool, str]:

        try:
            seed = SeedModel(name=name, quantity=quantity)
            seed_dict = seed.to_dict()
            seed_dict["item_type"] = "seed"
            seed_dict["updated_by"] = updated_by
            seed_dict["last_updated"] = datetime.datetime.now()
            seed_dict['condition'] = "available"
            await self.inventory_collection.insert_one(seed_dict)
            return True, f"Seed '{name}' added."
        except Exception as e:
            return False, str(e)

    async def plant_seed(self, seed_id: str, quantity: int) -> tuple[bool, str]:
        try:
            seed_data = self.inventory_collection.find_one({'_id': ObjectId(seed_id), "item_type": "seed"})
            if not seed_data:
                return False, "Seed not found."

            seed = SeedModel.from_dict(seed_data)
            if seed.quantity < quantity:
                return False, "Not enough seeds available."

            new_quantity = seed.quantity - quantity
            result =  self.inventory_collection.update_one(
                {'_id': ObjectId(seed_id), "item_type":"seed"},
                {'$set': {'quantity': new_quantity, "last_updated":datetime.datetime.now()}}
            )
            if result.modified_count == 1:
                return True, "Seed planted."
            return False, "Failed to update seed quantity."
        except Exception as e: return False, str(e)
    async def update_seed_quantity(self, seed_id: str, new_quantity: int) -> tuple[bool, str]:
        try:
            result =  self.inventory_collection.update_one(
                {'_id': ObjectId(seed_id), "item_type":"seed"},
                {'$set': {'quantity': new_quantity, "last_updated":datetime.datetime.now()}}
            )
            if result.modified_count == 1:
                return True, "Seed quantity updated."
            return False, "Seed not found or update failed."
        except Exception as e: return False, str(e)

    async def get_all_seeds(self) -> List[SeedModel]:
        seeds = []
        cursor = self.inventory_collection.find({"item_type": "seed"})
        for seed in cursor:
            seeds.append(SeedModel.from_dict(seed))
        return seeds

    async def remove_seed(self, seed_id: str) -> tuple[bool, str]:
        try:
            result =  self.inventory_collection.delete_one({'_id': ObjectId(seed_id), "item_type": "seed"})
            if result.deleted_count == 1: return True, "Seed removed."
            return False, "Seed not found."
        except Exception as e: return False, str(e)

