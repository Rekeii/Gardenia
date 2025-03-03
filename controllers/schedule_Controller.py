from schedule_Service import ScheduleService
from volunteer_Class import Volunteer
from task_Class import Task

class ScheduleController:
    def __init__(self):
        self.schedule_service = ScheduleService()

    def generate_schedule(self):
        self.schedule_service.generate_schedule()

    def assign_volunteer_to_schedule(self, volunteer: Volunteer, task: Task):
        self.schedule_service.assign_task_to_schedule(task, volunteer)

    def view_schedule(self):
        return self.schedule_service.schedule.scheduled_tasks
