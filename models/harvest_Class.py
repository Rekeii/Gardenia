from datetime import date
from plant_Class import Plant

class HarvestDistribution():
    def __init__(self):
        self.harvestedCrops = []
    
    def distributeHarvest(self):
        if not self.harvestedCrops:
            print("No crops to distribute.")
            return
        
        for crops in self.harvestedCrops:
            print(f"Dstributing {crops.name} {crops.type} harvested on {date.today()}")

        self.harvestedCrops.clear()

        

        