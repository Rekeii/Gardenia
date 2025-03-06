from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models.mongodb_client import MongoDBClient

class UserModel:
    def __init__(self, db_name='gardenia', login_collection='login', volunteers_collection='volunteers'):
        self.mongodb_client = MongoDBClient()
        self.db = self.mongodb_client.client[db_name]
        self.login_collection = self.db[login_collection]
        self.volunteers_collection = self.db[volunteers_collection]


    def authenticate(self, username, password):
        try:
            user = self.login_collection.find_one({'user': username, 'password': password})
            if user:
                if user['role'] == 'admin':
                    return {
                        'role': user['role'],
                        'username': username,
                        'name': 'Admin',  # Admin info directly
                        'specialization': 'N/A'
                    }
                else:  # It's a volunteer
                    volunteer = self.volunteers_collection.find_one({'user': username})
                    if volunteer:
                        return {
                            'role': user['role'],
                            'username': username,
                            'name': volunteer['name'],        # Get name from volunteers
                            'specialization': volunteer['specializations']  # Get specialization from volunteers, changed specializations to specialization
                        }
                    else:
                         return {
                            'role': user['role'],
                            'username': username,
                            'name': 'Volunteer',       # Default if no volunteer doc
                            'specialization': 'Not Assigned'  # Default
                        }
            return None  # User not found
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
                    'specializations': specialization #changed specialization to specializations
                }
                self.volunteers_collection.insert_one(volunteer_doc)

            return True, "User created successfully."

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False, f"Failed to create user: {str(e)}"

    def update_password(self, username: str, new_password: str):
        try:
            result = self.login_collection.update_one(
                {"user": username},
                {"$set": {"password": new_password}}
            )
            if result.matched_count == 1:
                return True, "Password updated successfully!"
            else:
                return False, "User not found or password not updated." # More specific message
        except Exception as e:
            print(f"Error updating password: {e}")
            return False, f"Failed to update password: {e}"


    def get_user_info(self, username: str):
        try:
            user = self.login_collection.find_one({'user': username})
            if not user:
                return None

            if user['role'] == 'admin':
                user_info = {
                    'role': user['role'],
                    'user': username,
                    'name': 'Admin',
                    'specialization': 'N/A'
                }
                return user_info
            else:  # It's a volunteer
                volunteer = self.volunteers_collection.find_one({'user': username})
                if volunteer:
                    user_info = {
                        'role': user['role'],
                        'user': username,
                        'name': volunteer['name'],
                        'specialization': volunteer['specializations']
                    }
                    return user_info
                else:
                    user_info = {
                        'role': user['role'],
                        'user': username,
                        'name': 'Volunteer',
                        'specialization': 'Not Assigned'
                    }
                    return user_info


        except Exception as e:
            print(f"Error retrieving user info: {str(e)}")
            return None
