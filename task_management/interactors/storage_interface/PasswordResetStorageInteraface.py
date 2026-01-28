from datetime import datetime
from abc import ABC, abstractmethod

from task_management.interactors.dtos import PasswordResetTokenDTO, UserDTO


class PasswordResetStorageInterface(ABC):

    @abstractmethod
    def create_password_reset_token(self, user_id: str, token: str,
                                    expires_at: datetime) -> PasswordResetTokenDTO:
        pass

    @abstractmethod
    def get_reset_token(self, token: str) -> PasswordResetTokenDTO | None:
        pass

    @abstractmethod
    def delete_reset_token(self, token: str) -> bool:
        pass

    @abstractmethod
    def update_user_password(self, user_id: str, new_password: str) -> UserDTO:
        pass