from django.contrib.auth.hashers import check_password

from task_management.exceptions.custom_exceptions import (
    EmailNotFound,
    InactiveUser,
    IncorrectPassword,
)
from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class UserLoginInteractor:

    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def user_login(self, email: str, password: str) -> UserDTO:
        user_dto = self._get_active_user_by_email(email=email)

        is_password_invalid = not self._is_password_matched(
            password=password,
            user_dto=user_dto,
        )
        if is_password_invalid:
            raise IncorrectPassword(password=password)

        return user_dto

    def _get_active_user_by_email(self, email: str) -> UserDTO:
        user_dto = self.user_storage.get_user_by_email(email=email)

        if not user_dto:
            raise EmailNotFound(email=email)

        if not user_dto.is_active:
            raise InactiveUser(user_id=user_dto.user_id)

        return user_dto

    @staticmethod
    def _is_password_matched(password: str, user_dto: UserDTO) -> bool:
        if check_password(password, user_dto.password):
            return True

        return user_dto.password == password
