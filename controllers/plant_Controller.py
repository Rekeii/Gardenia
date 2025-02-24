from plant_Class import PlantHealth, Plant
from plant_Service import PlantService

# Controller
class PlantController:
    @staticmethod
    def updatePlantHealthStatus(plant: Plant, newStatus:PlantHealth):
        PlantService.updateHealthStatus(plant, newStatus)
    
    @staticmethod
    def addNewPlant(plant):
        PlantService.addNewPlant(plant)
        print(f"Added new plant: {plant.name}")
    
    def getAllPlants():
        plants = PlantService.getAllPlants()
        if not plants:
            print("No plants available.")
        else:
            print("\nList of Plants: ")
            for plant in plants:
                print(plant)
    
    def removePlantFromSystem(plantID: str):
        print(f"Removing plant with ID {plantID} from the system.")