from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Seed:
    def __init__(self, db_name='gardenia', seed_collection='login'):
        # MongoDB connection setup
        uri = "mongodb+srv://gardenia_1:106lgardenia@cluster0.pmlml.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.seed_collection = self.db[seed_collection]

        # Test the connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Connection error: {str(e)}")

    def plant(self, quantity: int):
        if quantity > self.quantity:
            print(f"Not enough {self.name} seeds available!")
        else:
            self.quantity -= quantity
            print(f"Planted {quantity} {self.name} seeds. Remaining: {self.quantity}")
