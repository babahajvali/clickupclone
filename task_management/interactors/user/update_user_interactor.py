from task_management.exceptions.custom_exceptions import (
    EmailAlreadyExists,
    NothingToUpdateUser,
    PhoneNumberAlreadyExists,
    UsernameAlreadyExists,
)
from task_management.interactors.dtos import UpdateUserDTO, UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.mixins import UserValidationMixin


class UpdateUserInteractor(UserValidationMixin):

    def __init__(self, user_storage: UserStorageInterface):
        super().__init__(user_storage=user_storage)
        self.user_storage = user_storage

    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        self.check_user_is_active(user_id=update_user_dto.user_id)
        self._check_update_user_properties(update_user_dto=update_user_dto)

        return self.user_storage.update_user(update_user_dto=update_user_dto)

    def _check_update_user_properties(self,
                                      update_user_dto: UpdateUserDTO) -> None:
        has_no_fields_to_update = not self._has_fields_to_update(
            update_user_dto=update_user_dto,
        )
        if has_no_fields_to_update:
            raise NothingToUpdateUser(user_id=update_user_dto.user_id)

        self._check_username_not_taken_by_another_user(
            update_user_dto=update_user_dto,
        )
        self._check_email_not_taken_by_another_user(
            update_user_dto=update_user_dto,
        )
        self._check_phone_number_not_taken_by_another_user(
            update_user_dto=update_user_dto,
        )

    @staticmethod
    def _has_fields_to_update(update_user_dto: UpdateUserDTO) -> bool:
        return any([
            update_user_dto.username is not None,
            update_user_dto.email is not None,
            update_user_dto.phone_number is not None,
            update_user_dto.full_name is not None,
            update_user_dto.gender is not None,
            update_user_dto.image_url is not None,
        ])

    def _check_username_not_taken_by_another_user(
            self,
            update_user_dto: UpdateUserDTO) -> None:
        is_username_missing = update_user_dto.username is None
        if is_username_missing:
            return

        is_username_taken = (
            self.user_storage.check_username_except_current_user(
                user_id=update_user_dto.user_id,
                username=update_user_dto.username,
            )
        )
        if is_username_taken:
            raise UsernameAlreadyExists(username=update_user_dto.username)

    def _check_email_not_taken_by_another_user(
            self,
            update_user_dto: UpdateUserDTO) -> None:
        is_email_missing = update_user_dto.email is None
        if is_email_missing:
            return

        is_email_taken = (
            self.user_storage.check_email_exists_except_current_user(
                user_id=update_user_dto.user_id,
                email=update_user_dto.email,
            )
        )
        if is_email_taken:
            raise EmailAlreadyExists(email=update_user_dto.email)

    def _check_phone_number_not_taken_by_another_user(
            self,
            update_user_dto: UpdateUserDTO) -> None:
        is_phone_number_missing = update_user_dto.phone_number is None
        if is_phone_number_missing:
            return

        is_phone_number_taken = (
            self.user_storage.check_phone_number_except_current_user(
                user_id=update_user_dto.user_id,
                phone_number=update_user_dto.phone_number,
            )
        )
        if is_phone_number_taken:
            raise PhoneNumberAlreadyExists(
                phone_number=update_user_dto.phone_number,
            )
