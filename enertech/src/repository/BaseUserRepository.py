from abc import ABC, abstractmethod
from typing import List

from enertech.src.database.DatabaseManager import DatabaseManager
from enertech.src.domain.User import User


class BaseUserRepository(ABC):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def list_by_criteria(self, filters: dict) -> List[User]:
        pass
