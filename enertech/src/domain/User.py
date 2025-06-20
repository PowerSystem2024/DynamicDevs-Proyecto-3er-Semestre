from src.domain.UserRole import UserRole
from abc import ABC, abstractmethod  # Abstract Base Class for User


class User(ABC):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        self._id = None  # ID will be set by the database
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._active = True  # Default value for active status
        self._role = None  # the role will be determined by subclasses
        self._determine_role()

    # Getters
    @property
    def id(self) -> int:
        return self._id

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @property
    def is_active(self) -> bool:
        """
        Returns the active status of the user.
        """
        return self._active

    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Active status must be a boolean")
        self._active = value

    @property
    @abstractmethod
    def role(self) -> UserRole:
        """
        Returns the role of the user.
        This is a placeholder implementation and should be overridden in subclasses.
        """
        pass

    # Setters
    @first_name.setter
    def first_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("First name must be a string")
        self._first_name = value

    @last_name.setter
    def last_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Last name must be a string")
        self._last_name = value

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("Email must be a valid string")
        self._email = value

    @password.setter
    def password(self, value: str):
        if not isinstance(value, str) or len(value) < 8:
            raise ValueError("Password must be a string with at least 8 characters")
        self._password = value

    @abstractmethod
    def _determine_role(self):
        """
        Determines the role of the user based on their hierarchy or other criteria.
        This is a placeholder implementation and should be overridden in subclasses.
        """
        pass

    # represent the user as a string
    def __str__(self):
        return f"User(id={self._id}, name={self._first_name} {self._last_name}, role={self._role.value})"
