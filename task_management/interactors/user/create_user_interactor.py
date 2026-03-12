from task_management.exceptions.custom_exceptions import (
    EmailAlreadyExists,
    PhoneNumberAlreadyExists,
    UsernameAlreadyExists,
)
from task_management.interactors.dtos import CreateUserDTO, UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class CreateUserInteractor:

    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def create_user(self, create_user_dto: CreateUserDTO) -> UserDTO:
        self._check_username_not_taken(username=create_user_dto.username)
        self._check_email_not_taken(email=create_user_dto.email)
        self._check_phone_number_not_taken(
            phone_number=create_user_dto.phone_number,
        )

        return self.user_storage.create_user(user_data=create_user_dto)

    def _check_username_not_taken(self, username: str) -> None:
        is_username_taken = self.user_storage.check_username_exists(
            username=username,
        )
        if is_username_taken:
            raise UsernameAlreadyExists(username=username)

    def _check_email_not_taken(self, email: str) -> None:
        is_email_taken = self.user_storage.check_email_exists(email=email)
        if is_email_taken:
            raise EmailAlreadyExists(email=email)

    def _check_phone_number_not_taken(self, phone_number: str) -> None:
        is_phone_number_taken = self.user_storage.check_phone_number_exists(
            phone_number=phone_number,
        )
        if is_phone_number_taken:
            raise PhoneNumberAlreadyExists(phone_number=phone_number)
