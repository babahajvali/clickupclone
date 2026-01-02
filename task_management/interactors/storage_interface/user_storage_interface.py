from abc import ABC, abstractmethod

from task_management.interactors.dtos import UserDTO


class UserStorageInterface(ABC):

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_data(self, user_id: str)-> UserDTO:
        pass