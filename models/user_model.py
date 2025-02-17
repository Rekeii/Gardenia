from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class UserModel:
    def __init__(self, db_name='gardenia', login_collection='login', volunteers_collection='volunteers'):
        # MongoDB connection setup
        uri = "mongodb+srv://gardenia_1:106lgardenia@cluster0.pmlml.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.login_collection = self.db[login_collection]
        self.volunteers_collection = self.db[volunteers_collection]

        # Test the connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def authenticate(self, username, password):
        # Find the user in the login collection
        user = self.login_collection.find_one({'user': username, 'password': password})
        if user:
            # Fetch volunteer details using the 'id' field
            volunteer = self.volunteers_collection.find_one({'user': username})
            if volunteer:
                return {
                    'role': 'volunteer',  # Default role for now
                    'name': volunteer['name'],
                    'specialization': volunteer['specialization']
                }
        return None
