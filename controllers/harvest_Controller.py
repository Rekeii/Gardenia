from plant_Class import Plant
from harvest_Class import HarvestDistribution
from harvest_Service import HarvestDistributionService


class HarvestDistributionController:
    def __init__(self):
        self.harvestDistribution = HarvestDistribution()

    def distributeHarvest(self, crop: Plant, quantity: int):
        HarvestDistributionService.distributeHarvest(crop, quantity)

    def viewHarvestedCrops(self):
        if not self.harvestDistribution.harvestedCrops:
            print("No harvested crops to display.")
        else:
            print("\nList of Harvested Crops: ")
            for crop in self.harvestDistribution.harvestedCrops:
                print(f"{crop.name} ({crop.type})")