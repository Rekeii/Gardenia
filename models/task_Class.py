from __future__ import annotations 
from enum import Enum
from typing import Optional
from volunteer_Class import Volunteer

class Frequency (Enum):
    Daily = "daily"
    Monthly = "monthly

class TaskStatus(Enum):
    Pending = "Pending"
    Inprogress = "In Progress"
    Completed = "Completed"

class Task:
    def __init__(self, taskName: str, frequency:Frequency, assignedVolunteer: Volunteer, status: TaskStatus):
        self.taskName = taskName
        self.frequency = frequency
        self.assignedVolunteer: Optional [Volunteer] = None
        self.status = status

    def markComplete(self):
        self.status = TaskStatus.Completed

    def assignVolunteer(self, volunteer:Volunteer):
        self.assignedVolunteer = volunteer
        volunteer.assign_task(self)
