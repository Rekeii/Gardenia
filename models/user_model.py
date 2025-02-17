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
        user = self.login_collection.find_one({'user': username, 'password': password})
        if user:
            if user['role'] == 'admin':
                return {
                    'role': user['role'],
                    'username': username,
                    'name': 'Admin',  # Default name for admin
                    'specialization': 'N/A'  # No specialization for admin
                }
            else:
                volunteer = self.volunteers_collection.find_one({'user': username})
                if volunteer:
                    return {
                        'role': user['role'],
                        'username': username,
                        'name': volunteer['name'],
                        'specialization': volunteer['specialization']
                    }
                else:
                    # Return default values if volunteer record not found
                    return {
                        'role': user['role'],
                        'username': username,
                        'name': 'Volunteer',
                        'specialization': 'Not Assigned'
                    }
        return None

    
    def create_user(self, username, password, name, specialization, role):
        # Check if the user already exists
        if self.login_collection.find_one({'user': username}):
            return False, "User already exists."

        # Validate specialization (only for volunteers)
        valid_specializations = ["Pomology", "Olericulture", "Floriculture", "Landscaping", "PlantationCrops", "Versatile"]
        if role == 'volunteer' and specialization not in valid_specializations:
            return False, "Invalid specialization."

        # Create login document
        login_doc = {
            'user': username,
            'password': password,
            'role': role
        }
        self.login_collection.insert_one(login_doc)

        # Create volunteer document only for volunteers
        if role == 'volunteer':
            volunteer_doc = {
                'user': username,
                'name': name,
                'specialization': specialization
            }
            self.volunteers_collection.insert_one(volunteer_doc)

        return True, "User created successfully."


    def update_password(self, username, new_password):
        result = self.login_collection.update_one(
            {'user': username},
            {'$set': {'password': new_password}}
        )
        return result.modified_count > 0
