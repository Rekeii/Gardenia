# volunteer_model.py (Corrected)
from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId

class Specialization(str, Enum):
    Pomology = "pomology"
    Olericulture = "olericulture"
    Floriculture = "floriculture"
    Landscaping = "landscaping"
    PlantationCrops = "plantation_crops"
    Versatile = "versatile"

class Frequency(str, Enum):
    Daily = "daily"
    Monthly = "monthly"

class TaskStatus(str, Enum):
    Pending = "Pending"
    InProgress = "In Progress"
    Completed = "Completed"

class Task:
    def __init__(self, taskName: str, frequency: Frequency,
                 assignedVolunteerId: Optional[str] = None,
                 status: TaskStatus = TaskStatus.Pending,
                 _id: Optional[ObjectId] = None):
        self.taskName = taskName
        self.frequency = frequency
        self.assignedVolunteerId = assignedVolunteerId
        self.status = status
        self._id = _id

    def markComplete(self):
        self.status = TaskStatus.Completed

    def to_dict(self) -> Dict:
        data = {
            "taskName": self.taskName,
            "frequency": self.frequency.value,
            "assignedVolunteerId": self.assignedVolunteerId,
            "status": self.status.value,
        }
        if self._id:
            data['_id'] = self._id
        return data

    @classmethod
    def from_dict(cls, data:Dict):
        return Task(
            taskName = data.get('taskName', 'Unknown Task'),
            frequency= Frequency(data.get('frequency', 'daily')),
            assignedVolunteerId = data.get('assignedVolunteerId'),
            status = TaskStatus(data.get('status', 'Pending')),
            _id = data.get('_id')
        )

class Volunteer:
    def __init__(self, name: str, specialization: Specialization,
                 tasks_assigned: Optional[List[str]] = None,
                 _id: Optional[ObjectId] = None):
        self.name = name
        self.specialization = specialization
        self.tasks_assigned = tasks_assigned or []
        self._id = _id

    def assignTask(self, task_id: str):
        self.tasks_assigned.append(task_id)

    def logFindings(self, notes: str):
        print(f"Findings logged by {self.name}: {notes}")

    def to_dict(self) -> Dict:
        data = {
            "name": self.name,
            "specializations": self.specialization.value,  # Store lowercase
            "tasks_assigned": self.tasks_assigned,
        }
        if self._id:
            data['_id'] = self._id
        return data

    @classmethod
    def from_dict(cls, data: Dict):
        return Volunteer(
            name=data.get('name', "Unknown volunteer"),
            specialization=Specialization(data.get('specializations', 'versatile').lower()),  # Lowercase here
            tasks_assigned=data.get('tasks_assigned', []),
            _id=data.get('_id')
        )

class Schedule:
    def __init__(self):
        self.scheduled_tasks: List[Task] = []

    def generate_schedule(self):
        print("Schedule generated.")

    def assign_volunteers(self):
        print("Volunteers assigned to schedule.")
