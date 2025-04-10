from flask_login import UserMixin
from abc import ABC, abstractmethod

class AbstractUser(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    def is_admin(self) -> bool:
        return False


class User(UserMixin, AbstractUser):
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return self.id


class AdminUser(User):
    def is_admin(self) -> bool:
        return True
