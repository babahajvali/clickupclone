from django.contrib.auth.hashers import check_password

from task_management.exceptions.custom_exceptions import \
    EmailNotFound, IncorrectPassword, \
    UsernameAlreadyExists, EmailAlreadyExists, \
    PhoneNumberAlreadyExists, InactiveUser, NothingToUpdateUser
from task_management.interactors.dtos import CreateUserDTO, UserDTO, \
    UpdateUserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.mixins import UserValidationMixin


class UserInteractor:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage
        self.user_mixin = UserValidationMixin(user_storage=user_storage)

    def create_user(self, user_details: CreateUserDTO) -> UserDTO:

        self._is_username_taken(user_details.username)
        self._is_email_registered(email=user_details.email)
        self._is_phone_number_exists(phone_number=user_details.phone_number)

        return self.user_storage.create_user(user_data=user_details)

    def update_user(self, user_update_data: UpdateUserDTO) -> UserDTO:

        self.user_mixin.check_user_is_active(user_id=user_update_data.user_id)
        self._check_update_user_field_properties(user_data=user_update_data)

        return self.user_storage.update_user(user_data=user_update_data)

    def get_user_profile(self, user_id: str) -> UserDTO:

        self.user_mixin.check_user_is_active(user_id=user_id)

        return self.user_storage.get_user(user_id=user_id)

    def block_user(self, user_id: str) -> UserDTO:

        self.user_mixin.check_user_is_active(user_id=user_id)

        return self.user_storage.block_user(user_id=user_id)

    def user_login(self, email: str, password: str) -> UserDTO:

        is_email_exist = self.user_storage.check_email_exists(email=email)

        if not is_email_exist:
            raise EmailNotFound(email=email)
        user_data = self.user_storage.get_user_by_email(email=email)

        if not user_data.is_active:
            raise InactiveUser(user_id=user_data.user_id)

        if check_password(password, user_data.password):
            return user_data

        # Backward compatibility for old plain-text records.
        if user_data.password == password:
            return user_data

        raise IncorrectPassword(password=password)

    def _is_username_taken(self, username: str):
        is_existed_username = self.user_storage.check_username_exists(
            username=username)

        if is_existed_username:
            raise UsernameAlreadyExists(username=username)

    def _is_email_registered(self, email: str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if is_existed_email:
            raise EmailAlreadyExists(email=email)

    def _is_phone_number_exists(self, phone_number: str):
        is_existed_phone_number = self.user_storage.check_phone_number_exists(
            phone_number=phone_number)

        if is_existed_phone_number:
            raise PhoneNumberAlreadyExists(phone_number=phone_number)

    def _check_username_except_current_user(self, username: str,
                                            user_id: str):
        is_user_exist_username = (
            self.user_storage.check_username_except_current_user(
                user_id=user_id, username=username))

        if is_user_exist_username:
            raise UsernameAlreadyExists(username=username)

    def _check_email_except_current_user(self, user_id: str, email: str):

        is_user_exist_email = (
            self.user_storage.check_email_exists_except_current_user(
                user_id=user_id, email=email))

        if is_user_exist_email:
            raise EmailAlreadyExists(email=email)

    def _check_phone_number_except_current_user(self, user_id: str,
                                                phone_number: str):

        is_user_exist_phone_number = (
            self.user_storage.check_phone_number_except_current_user(
                user_id=user_id, phone_number=phone_number))

        if is_user_exist_phone_number:
            raise PhoneNumberAlreadyExists(phone_number=phone_number)

    def _check_update_user_field_properties(self, user_data: UpdateUserDTO):

        if not self._has_at_least_one_field_to_update(user_data=user_data):
            raise NothingToUpdateUser(user_id=user_data.user_id)

        is_username_provided = user_data.username is not None
        if is_username_provided:
            self._check_username_except_current_user(
                username=user_data.username, user_id=user_data.user_id)

        is_email_provided = user_data.email is not None
        if is_email_provided:
            self._check_email_except_current_user(
                email=user_data.email, user_id=user_data.user_id)

        is_phone_number_provided = user_data.phone_number is not None
        if is_phone_number_provided:
            self._check_phone_number_except_current_user(
                user_id=user_data.user_id, phone_number=user_data.phone_number)

    @staticmethod
    def _has_at_least_one_field_to_update(user_data: UpdateUserDTO) -> bool:
        return any([
            user_data.username is not None,
            user_data.email is not None,
            user_data.phone_number is not None,
            user_data.full_name is not None,
            user_data.gender is not None,
            user_data.image_url is not None
        ])
