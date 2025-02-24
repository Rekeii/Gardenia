from plant_Class import Plant, PlantType, PlantHealth

# Service
class PlantService:
    plants = []
    # to store plants

    @staticmethod
    def updatePlantHealthStatus(plant: Plant, newStatus:PlantHealth):
        plant.updateHealthStatus(newStatus)

    @staticmethod
    def trackPlantGrowth(plant:Plant):
        print(f"Tracking Plant Growth for {plant.name}. Estimated harvest date: {plant.estimatedHarvestDate}.")

    @staticmethod
    def addNewPlant(plant:Plant):
        PlantService.plants.append(plant)
    
    @staticmethod
    def getAllPlants():
        return PlantService.plants