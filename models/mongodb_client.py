from pymongo import MongoClient
from datetime import datetime
import os

class MongoDBClient:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.connect()
        return cls.__instance

    def connect(self):
        uri = os.getenv('MONGODB_URI', "mongodb+srv://gardenia_1:106lgardenia@cluster0.pmlml.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.client = MongoClient(uri)
        self.gardenia_db = self.client['gardenia']
        self.plants_collection = self.gardenia_db['plants']
        self.volunteers_collection = self.gardenia_db['volunteers']
        self.login_collection = self.gardenia_db['login']
        self.harvests_collection = self.gardenia_db['harvests']

        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")

    def get_plants_collection(self):
        return self.plants_collection

    def get_volunteers_collection(self):
        return self.volunteers_collection

    def get_login_collection(self):
        return self.login_collection

    def get_harvests_collection(self):
        return self.harvests_collection

    def close_connection(self):
        self.client.close()
