from tool_class import ToolModel, ToolCondition
from models.mongodb_client import MongoDBClient
import asyncio
from bson import ObjectId
from typing import List, Optional

class ToolServiceController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.tool_collection = self.mongodb_client.tool_collection

    async def add_tool(self, name: str, condition: ToolCondition) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            tool = ToolModel(name=name, condition=condition)
            tool_dict = tool.to_dict()
            result = await loop.run_in_executor(None, self.tool_collection.insert_one, tool_dict)
            return True, f"Tool '{name}' added. ID: {result.inserted_id}"
        except Exception as e:
            return False, str(e)

    async def repair_tool(self, tool_id: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(
                None,
                self.tool_collection.update_one,
                {'_id': ObjectId(tool_id)},
                {'$set': {'condition': ToolCondition.Good}}
            )
            if result.modified_count == 1:
                return True, "Tool repaired."
            return False, "Tool not found or already in good condition."
        except Exception as e:
            return False, str(e)

    async def get_all_tools(self) -> List[ToolModel]:
        loop = asyncio.get_running_loop()
        try:
            cursor = await loop.run_in_executor(None, self.tool_collection.find)
            return [ToolModel.from_dict(tool) for tool in cursor]
        except Exception as e:
            print(f"Error: {e}")
            return []

    async def remove_tool(self, tool_id: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(None, self.tool_collection.delete_one, {'_id': ObjectId(tool_id)})
            if result.deleted_count == 1:
                return True, "Tool removed."
            return False, "Tool not found."
        except Exception as e:
            return False, str(e)
