from models.user_model import UserModel

class LoginController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, username, password):
        user_info = self.user_model.authenticate(username, password)
        if user_info:
            return user_info
        return None
<<<<<<< HEAD

    def update_password(self, username, new_password):
        return self.user_model.update_password(username, new_password)

=======
>>>>>>> refs/remotes/origin/prod1
