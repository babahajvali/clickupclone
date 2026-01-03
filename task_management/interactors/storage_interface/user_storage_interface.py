from abc import ABC, abstractmethod

from task_management.interactors.dtos import UserDTO, CreateUserDTO


class UserStorageInterface(ABC):

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_data(self, user_id: str)-> UserDTO:
        pass

    @abstractmethod
    def get_user_details(self, email: str) -> UserDTO:
        pass

    @abstractmethod
    def create_user(self, user_data: CreateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def update_user(self, user_data: UserDTO) -> UserDTO:
        pass

    @abstractmethod
    def block_user(self, user_id: str) -> UserDTO:
        pass

    @abstractmethod
    def check_username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def check_email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def check_phone_number_exists(self, phone_number: str) -> bool:
        pass

    @abstractmethod
    def check_user_username_exists(self, user_id: str, username: str) -> bool:
        pass

    @abstractmethod
    def check_user_email_exists(self, user_id: str, email: str) -> bool:
        pass

    @abstractmethod
    def check_user_phone_number_exists(self, user_id: str,
                                       phone_number: str) -> bool:
        pass