from models.volunteer_model import Volunteer, Task, Specialization, Frequency, TaskStatus
from models.mongodb_client import MongoDBClient
from bson import ObjectId
import asyncio
from typing import List, Optional, Dict
from datetime import datetime
from controllers.inventory_controller import InventoryController
from controllers.harvest_controller import HarvestController
from models.inventory_model import InventoryModel  # Add this import if not present

class VolunteerController:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.volunteers_collection = self.mongodb_client.volunteers_collection
        self.tasks_collection = self.mongodb_client.tasks_collection

    async def add_volunteer(self, user: str, name: str, specialization: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            specialization_enum = Specialization(specialization.lower())
            volunteer = Volunteer(user=user, name=name, specialization=specialization_enum)
            result = await loop.run_in_executor(None, self.volunteers_collection.insert_one, volunteer.to_dict())
            return True, f"Volunteer added with ID: {result.inserted_id}"
        except ValueError as e:
            return False, f"Invalid specialization: {e}"
        except Exception as e:
            return False, str(e)
        
    async def remove_volunteer(self, volunteer_id: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            result = await loop.run_in_executor(None, self.volunteers_collection.delete_one, {'_id': ObjectId(volunteer_id)})
            if result.deleted_count == 1:
                return True, "Volunteer removed successfully."
            else:
                return False, "Volunteer not found."
        except Exception as e:
            return False, str(e)
        
    async def get_volunteer(self, volunteer_id: str) -> Optional[Volunteer]:
        loop = asyncio.get_running_loop()
        try:
            volunteer_data = await loop.run_in_executor(None, self.volunteers_collection.find_one, {'_id': ObjectId(volunteer_id)})
            if volunteer_data:
                return Volunteer.from_dict(volunteer_data)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def get_volunteer_by_name(self, name: str) -> Optional[Volunteer]:
        loop = asyncio.get_running_loop()
        try:
            volunteer_data = await loop.run_in_executor(None, self.volunteers_collection.find_one, {'name': name})
            if volunteer_data:
                return Volunteer.from_dict(volunteer_data)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def get_all_volunteers(self) -> List[Volunteer]:
        loop = asyncio.get_running_loop()
        try:
            volunteers = []
            cursor =  await loop.run_in_executor(None, self.volunteers_collection.find, {})
            for volunteer_data in cursor:
                volunteers.append(Volunteer.from_dict(volunteer_data))
            return volunteers
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    async def assign_task_to_volunteer(self, volunteer_id: str, task_id: str) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            volunteer_update_result = await loop.run_in_executor(
                None,
                self.volunteers_collection.update_one,
                {'_id': ObjectId(volunteer_id)},
                {'$push': {'tasks_assigned': task_id}}
            )

            task_update_result = await loop.run_in_executor(
                None,
                self.tasks_collection.update_one,
                {'_id': ObjectId(task_id)},
                {'$set': {'assignedVolunteerId': volunteer_id}}
            )

            if volunteer_update_result.modified_count == 1 and task_update_result.modified_count == 1:
                return True, "Task assigned successfully."
            else:
                return False, "Failed to assign task. Volunteer or Task not found, or update failed."
        except Exception as e:
            return False, str(e)

    async def get_volunteer_tasks(self, volunteer_id: str) -> List[Task]:
        loop = asyncio.get_running_loop()
        try:
            volunteer = await self.get_volunteer(volunteer_id)
            if not volunteer:
                return []

            cursor = await loop.run_in_executor(
                None,
                self.tasks_collection.find,
                {'_id': {'$in': [ObjectId(task_id) for task_id in volunteer.tasks_assigned]}}
            )
            tasks = []
            for task_data in cursor:
                tasks.append(Task.from_dict(task_data))
            return tasks
        except Exception as e:
            print(f"Error: {e}")
            return []

    async def add_task(self, taskName: str, frequency: str, assignedVolunteerId: Optional[str] = None) -> tuple[bool, str]:
        loop = asyncio.get_running_loop()
        try:
            # Create the Task object
            task = Task(
                taskName=taskName,
                frequency=Frequency(frequency),
                assignedVolunteerId=assignedVolunteerId
            )
            task_dict = task.to_dict()

            # Insert the task into the tasks collection
            task_result = await loop.run_in_executor(
                None,
                self.tasks_collection.insert_one,
                task_dict
            )
            task_id = str(task_result.inserted_id)

            if assignedVolunteerId is not None:
                # Update the volunteer's tasks_assigned array
                volunteer_update = await loop.run_in_executor(
                    None,
                    self.volunteers_collection.update_one,
                    {'_id': ObjectId(assignedVolunteerId)},
                    {'$push': {'tasks_assigned': task_id}}
                )

                if volunteer_update.modified_count != 1:
                    # Rollback if volunteer update failed
                    await loop.run_in_executor(
                        None,
                        self.tasks_collection.delete_one,
                        {'_id': task_result.inserted_id}
                    )
                    return False, "Failed to assign task to volunteer"

            return True, f"Task '{taskName}' added successfully. ID: {task_id}"

        except Exception as e:
            return False, str(e)

    async def get_task(self, taskID) -> Optional[Task]:
        loop = asyncio.get_running_loop()
        try:
            task = await loop.run_in_executor(None, self.tasks_collection.find_one, {'_id': ObjectId(taskID)})
            if task:
                return Task.from_dict(task)
            return None
        except Exception as e:
            print(f"Error retrieving task document: {e}")
            return None
        
    async def get_all_tasks(self) -> List[Task]:
            loop = asyncio.get_running_loop()
            try:
                tasks = []

                cursor = await loop.run_in_executor(None, self.tasks_collection.find)
                for task_data in cursor:
                    tasks.append(Task.from_dict(task_data))
                return tasks
            except Exception as e:
                print(f"Error: {e}")
                return []

    async def mark_task_complete(self, task_id: str) -> tuple[bool, str]:
        try:
            task = await self.get_task(task_id)
            if not task:
                return False, "Task not found"

            # Check if this is a harvest task
            if task.plant_id:  # If task has associated plant
                harvest_controller = HarvestController()
                success, msg = await harvest_controller.mark_ready_for_harvest(task.plant_id)
                if not success:
                    return False, f"Failed to process harvest: {msg}"

            # Mark task as complete
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,
                self.tasks_collection.update_one,
                {'_id': ObjectId(task_id)},
                {
                    '$set': {
                        'status': TaskStatus.Completed.value,
                        'completed_at': datetime.now()
                    }
                }
            )

            if result.modified_count == 1:
                return True, "Task completed successfully"
            return False, "Failed to update task status"
                
        except Exception as e:
            return False, str(e)

    async def close_connection(self) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.mongodb_client.close_connection)