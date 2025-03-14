from models.user_model import UserModel
import asyncio

class LoginController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, username, password):
        return self.user_model.authenticate(username, password)

    async def update_password(self, username: str, new_password: str) -> tuple[bool, str]:
        """Asynchronous password update handler"""
        try:
            if not self._validate_password(new_password):
                return False, "Password must be at least 4 characters"
            
            update_result = await asyncio.get_event_loop().run_in_executor(
                None, 
                self.user_model.update_password, 
                username, 
                new_password
            )
            return update_result
        except Exception as e:
            return False, f"Update failed: {str(e)}"

    def _validate_password(self, password: str) -> bool:
        return len(password) >= 4
