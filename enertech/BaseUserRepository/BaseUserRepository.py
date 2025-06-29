from abc import ABC, abstractmethod
from typing import Optional, Dict, List

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
    def list_by_criteria(self, filters: Optional[Dict[str, any]] = None, sort: str = "id") -> Optional[List[User]]:
        pass
