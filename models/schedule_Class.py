from typing import List
from task_Class import Task

class Schedule:
    def __init__(self):
        self.scheduled_tasks: List[Task] = []

    def generate_schedule(self):
        print("Schedule generated.")

    def assign_volunteers(self):
        print("Volunteers assigned to schedule.")
