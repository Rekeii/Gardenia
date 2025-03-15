#user_model
from models.mongodb_client import MongoDBClient

class UserModel:
    def __init__(self):
        self.mongodb_client = MongoDBClient()
        self.login_collection = self.mongodb_client.get_login_collection()  # Updated to use method
        self.volunteers_collection = self.mongodb_client.get_volunteers_collection()  # Updated to use method

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
                            'specialization': volunteer['specializations']
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
                    'specializations': specialization 
                }
                self.volunteers_collection.insert_one(volunteer_doc)

            return True, "User created successfully."

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False, f"Failed to create user: {str(e)}"

    def update_password(self, username: str, new_password: str) -> tuple[bool, str]:
        """Update password in database"""
        if not self._validate_password(new_password):
            return False, "Password too weak"
        
        try:
            # Update operation
            result = self.login_collection.update_one(
                {"user": username},
                {"$set": {"password": self._hash_password(new_password)}}
            )
            
            if result.matched_count == 1:
                return True, "Password updated successfully!"
            else:
                return False, "User not found"
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            return False, "Internal server error"
    
    def _validate_password(self, password: str) -> bool:
        """Add password validation logic here"""
        return len(password) >= 4  # Simple muna
    
    def _hash_password(self, password: str) -> str:
        """Add proper password hashing here"""
        return password  # TO-DO: Replace with actual hashing


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
