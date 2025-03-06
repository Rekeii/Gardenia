from pymongo import MongoClient
from datetime import datetime
import os

class MongoDBClient:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.connect()
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                #  TO-DO: Exception handling here
                raise  # Re-raise the exception to stop execution
        return cls._instance

    def connect(self):
        # This is unsecure but TO-DO.
        uri = os.getenv('MONGODB_URI', "mongodb+srv://gardenia_1:106lgardenia@cluster0.pmlml.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.client = MongoClient(uri)
        self.gardenia_db = self.client['gardenia']
        self.plants_collection = self.gardenia_db['plants']
        self.volunteers_collection = self.gardenia_db['volunteers']
        self.login_collection = self.gardenia_db['login']
        self.harvests_collection = self.gardenia_db['harvests']
        self.inventory_collection = self.gardenia_db['inventory']  # Add this line
        self.tasks_collection = self.gardenia_db['tasks'] #Add this line

        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")
            raise # prevent continuing with a broken connection

    def get_plants_collection(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB plants.")
            return self.plants_collection
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")
            return

    def get_volunteers_collection(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB volunteers_collection.")
            return self.volunteers_collection
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")
            return

    def get_login_collection(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB login_collection.")
            return self.login_collection
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")
            return

    def get_harvests_collection(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB harvests_collection.")
            return self.harvests_collection
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")
            return
    def get_inventory_collection(self): #add this
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB inventory_collection")
            return self.inventory_collection
        except Exception as e:
            print(f"MongoDB Connection error: {str(e)}")
            return
    def get_tasks_collection(self): #add this
        try:
            self.client.admin.command('ping')
            print("Successfully connected to Task Collection")
            return self.tasks_collection
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")
