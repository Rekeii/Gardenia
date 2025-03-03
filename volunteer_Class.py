from enum import Enum

class Specialization(str, Enum):
    Pomology = "Pomology"
    Olericulture = "Olericulture"
    Floriculture = "Floriculture"
    Landscaping = "Landscaping"
    PlantationCrops = "Plantation_Crops"
    Versatile= "Versatile"


class Volunteer:
    def __init__(self, name: str, specialization: Specialization):
        self.name = name
        self.specialization = specialization
        self.tasks_assigned =[]

    def assignTask(self, task):
        self.tasks_assigned.append(task)

    def logFindings(self, notes: str):
        print(f"Findings logged by {self.name}: {notes}")
