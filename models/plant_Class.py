from datetime import date
from enum import Enum

# Plant Model
class PlantType(str, Enum):
    FRUIT = 'Fruit'
    VEGETABLE = 'Vegetable'
    FLOWER = 'Flower'
    HERB = 'Herb'
    OTHER = 'Other'

class PlantHealth(str, Enum):
    HEALTHY = 'Healthy'
    NEEDS_WATER = 'Needs Water'
    PESTS_DETECTED = 'Pests Detected'
    READY_FOR_HARVEST = 'Ready For Harvest'

class Plant:
    def __init__(self, name:str, type:PlantType, plantingDate:date, estimatedHarvestDate: date, location: str, healthStatus:PlantHealth):
        self.name = name
        self.type = type
        self.plantingDate = plantingDate
        self.estimatedHarvestDate = estimatedHarvestDate
        self.location = location
        self.healthStatus = healthStatus

    def __str__(self):
        return f"{self.name} ({self.type}) - Planted on {self.plantingDate}, Estimated Harvest: {self.estimatedHarvestDate}, Location: {self.location}, Status: {self.healthStatus}"
    
    def updateHealthStatus(self, newStatus: PlantHealth):
        self.healthStatus = newStatus



    
