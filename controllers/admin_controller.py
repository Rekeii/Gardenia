from models.user_model import UserModel

class AdminController:
    def __init__(self):
        self.user_model = UserModel()

    def create_user(self, username, password, name, specialization, role):
        return self.user_model.create_user(username, password, name, specialization, role)
