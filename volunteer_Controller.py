from volunteer_service import VolunteerService
from volunteer_Class import Volunteer

class VolunteerController:
    def __init__(self):
        self.volunteer_service = VolunteerService()

    def addVolunteer(self, volunteer: Volunteer):
        self.volunteer_service.add_volunteer(volunteer)

    def removeVolunteer(self, volunteerId: str):
        self.volunteer_service.remove_volunteer(volunteerId)

    def getAssignedTask(self, volunteerId: str):
        return self.volunteer_service.get_assigned_tasks(volunteerId)
