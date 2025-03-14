from models.user_model import UserModel

class LoginController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, username, password):
        user_info = self.user_model.authenticate(username, password)
        if user_info:
            return user_info
        return None

    async def update_password(self, username, new_password):
        """Asynchronous password update handler"""
        loop = asyncio.get_event_loop()
        success, message = await loop.run_in_executor(
            None, 
            self.user_model.update_password, 
            username, 
            new_password
        )
        return success, message

