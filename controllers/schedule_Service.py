from schedule_Class import Schedule
from volunteer_Class import  Volunteer
from task_Class import Task

class ScheduleService:
    def __init__(self):
        self.schedule = Schedule()

    def generate_schedule(self):
        self.schedule.generate_schedule()

    def assign_task_to_schedule(self, task: Task, volunteer: Volunteer):
        task.assign_volunteer = volunteer
        self.schedule.scheduled_tasks.append(task)
