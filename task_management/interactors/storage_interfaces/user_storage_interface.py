from abc import ABC, abstractmethod
from datetime import datetime

from task_management.interactors.dtos import UserDTO, CreateUserDTO, \
    UpdateUserDTO, PasswordResetTokenDTO


class UserStorageInterface(ABC):


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
    def update_user(self, user_data: UpdateUserDTO) -> UserDTO:
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
    def check_username_except_current_user(self, user_id: str, username: str) -> bool:
        pass

    @abstractmethod
    def check_email_exists_except_current_user(self, user_id: str, email: str) -> bool:
        pass

    @abstractmethod
    def check_phone_number_except_current_user(self, user_id: str,
                                               phone_number: str) -> bool:
        pass

    @abstractmethod
    def check_user_exists(self, user_id: str)-> bool:
        pass

    @abstractmethod
    def create_password_reset_token(self, user_id: str, token: str,
                                    expires_at: datetime) -> PasswordResetTokenDTO:
        pass

    @abstractmethod
    def get_reset_token(self, token: str) -> PasswordResetTokenDTO | None:
        pass

    @abstractmethod
    def used_reset_token(self, token: str) -> bool:
        pass

    @abstractmethod
    def update_user_password(self, user_id: str, new_password: str) -> UserDTO:
        pass