from enum import Enum

class Specialization(str, Enum):
    Pomology = "pomology"
    Olericulture = "olericulture"
    Floriculture = "floriculture"
    Landscaping = "landscaping"
    PlantationCrops = "plantation_crops"
    Versatile= "versatile"


class Volunteer:
    def __init__(self, name: str, specialization: Specialization):
        self.name = name
        self.specialization = specialization
        self.tasks_assigned =[]

    def assignTask(self, task):
        self.tasks_assigned.append(task)

    def logFindings(self, notes: str):
        print(f"Findings logged by {self.name}: {notes}")
