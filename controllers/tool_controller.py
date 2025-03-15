# controllers/tool_controller.py
from models.tool_model import ToolModel, ToolCondition
from models.mongodb_client import MongoDBClient
from bson import ObjectId
from typing import List, Optional
import asyncio, datetime

class ToolServiceController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.inventory_collection = self.mongodb_client.inventory_collection  # Use inventory

    async def add_tool(self, name: str, condition: ToolCondition, updated_by: str) -> tuple[bool, str]:
        try:
            tool = ToolModel(name=name, condition=condition)
            tool_dict = tool.to_dict()
            tool_dict["item_type"] = "tool"  # Use item_type
            tool_dict["updated_by"] = updated_by
            tool_dict["last_updated"] = datetime.datetime.now()
            tool_dict["condition"] = condition.value  # Use condition.value
            # tool_dict["status"] = condition.value # Status removed use only condition

            await self.inventory_collection.insert_one(tool_dict)
            return True, f"Tool '{name}' added."
        except Exception as e:
            return False, str(e)

    async def repair_tool(self, tool_id: str) -> tuple[bool, str]:
        try:
            result =  self.inventory_collection.update_one(
                {'_id': ObjectId(tool_id), "item_type": "tool"},
                {'$set': {'condition': ToolCondition.Good.value, 'last_updated': datetime.datetime.now()}}
            )
            if result.modified_count == 1:
                return True, "Tool repaired."
            return False, "Tool not found or already in good condition."
        except Exception as e:
            return False, str(e)


    async def get_all_tools(self) -> List[ToolModel]:
        tools = []
        cursor =  self.inventory_collection.find({"item_type": "tool"}) # cursor and no awiat
        for tool in cursor: # Regular for loop
            tools.append(ToolModel.from_dict(tool))
        return tools
    
    async def remove_tool(self, tool_id: str) -> tuple[bool, str]:
        try:
            result = self.inventory_collection.delete_one({'_id': ObjectId(tool_id), "item_type": "tool"})
            if result.deleted_count == 1:
                return True, "Tool removed."
            return False, "Tool not found."
        except Exception as e:
            return False, str(e)
