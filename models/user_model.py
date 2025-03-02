from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class UserModel:
    def __init__(self, db_name='gardenia', login_collection='login', volunteers_collection='volunteers'):
        self.mongodb_client = MongoDBClient()
        self.db = self.mongodb_client.client[db_name]
        self.login_collection = self.db[login_collection]
        self.volunteers_collection = self.db[volunteers_collection]

        # Test the connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Connection error: {str(e)}")

    def authenticate(self, username, password):
        try:
            user = self.login_collection.find_one({'user': username, 'password': password})
            if user:
                if user['role'] == 'admin':
                    return {
                        'role': user['role'],
                        'username': username,
                        'name': 'Admin',
                        'specialization': 'N/A'
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
                        return {
                            'role': user['role'],
                            'username': username,
                            'name': 'Volunteer',
                            'specialization': 'Not Assigned'
                        }
            return None
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None

    def create_user(self, username, password, name, specialization, role):
        try:
            # Check if the username already exists in login or volunteers
            if self.login_collection.find_one({'user': username}) or self.volunteers_collection.find_one({'user': username}):
                return False, "Username already exists."

            # Validate specialization for volunteers
            valid_specializations = ["Pomology", "Olericulture", "Floriculture", "Landscaping", "PlantationCrops", "Versatile"]
            if role == 'volunteer' and specialization not in valid_specializations:
                return False, "Invalid specialization."

            # Create user in login collection
            login_doc = {
                'user': username,
                'password': password,
                'role': role
            }
            self.login_collection.insert_one(login_doc)

            # Create volunteer document if the role is volunteer
            if role == 'volunteer':
                volunteer_doc = {
                    'user': username,
                    'name': name,
                    'specialization': specialization
                }
                self.volunteers_collection.insert_one(volunteer_doc)

            return True, "User created successfully."

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False, f"Failed to create user: {str(e)}"

    def update_password(self, username: str, new_password: str):
        result = self.login_collection.update_one(
            {"user": username},
            {"$set": {"password": new_password}}
        )
        return result.matched_count == 1, "Password updated successfully!"

    def get_user_info(self, username: str):
        try:
            user = self.login_collection.find_one({'user': username})
            if not user:
                return None
            user_info = {
                'role': user['role'],
                'user': username,
                'name': user.get('name', 'Volunteer'),
                'specialization': user.get('specialization', 'Not Assigned')
            }
            return user_info
        except Exception as e:
            print(f"Error retrieving user info: {str(e)}")
            return None
        