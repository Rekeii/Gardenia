from datetime import date
from plant_Class import Plant

class HarvestDistributionService:
    @staticmethod
    def distributeHarvest(crop: Plant, quantity: int):
        print(f"Distributing {quantity} units of {crop.name} ({crop.type}) harvested on {date.today()}.")
