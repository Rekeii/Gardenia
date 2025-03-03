
from typing import List, Dict
from volunteer_Class import Volunteer
from task_Class import Task

class VolunteerController:
    def __init__(self):
        self.volunteers: Dict[str, Volunteer] = {}  

    def add_volunteer(self, volunteer: Volunteer):
        self.volunteers[volunteer.name] = volunteer  

    def remove_volunteer(self, volunteerId: str):
        self.volunteers.pop(volunteerId, None)  

    def get_assigned_tasks(self, volunteerId: str) -> List[str]:
        return self.volunteers.get(volunteerId, Volunteer("", "")).assign_task
    
       