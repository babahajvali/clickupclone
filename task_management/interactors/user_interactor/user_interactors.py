from task_management.exceptions.custom_exceptions import NotExistedEmailFound, \
    WrongPasswordFound, ExistedUsernameFound, ExistedEmailFound, \
    ExistedPhoneNumberFound, UsernameNotFound
from task_management.interactors.dtos import CreateUserDTO, UserDTO
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UserInteractor(ValidationMixin):
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def create_user(self, user_details: CreateUserDTO) -> UserDTO:
        self._validate_username_not_taken(user_details.username)
        self._validate_email_not_registered(email=user_details.email)
        self._validate_phone_number_not_exists(phone_number=user_details.phone_number)

        return self.user_storage.create_user(user_data=user_details)

    def update_user(self, user_update_data: UserDTO) -> UserDTO:
        user_id = user_update_data.user_id
        self.validate_user_is_active(user_id=user_update_data.user_id,
                                      user_storage=self.user_storage)
        self._validate_updated_username_unique(username=user_update_data.username, user_id=user_id)
        self._validate_updated_email_unique(email=user_update_data.email, user_id=user_id)
        self._validate_updated_phone_number_unique(user_id=user_id,
                                                   phone_number=user_update_data.phone_number)

        return self.user_storage.update_user(user_data=user_update_data)

    def get_user_profile(self, user_id: str) -> UserDTO:
        self.validate_user_is_active(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.get_user_data(user_id=user_id)

    def block_user(self, user_id: str) -> UserDTO:
        self.validate_user_is_active(user_id=user_id, user_storage=self.user_storage)

        return self.user_storage.block_user(user_id=user_id)

    def user_login(self, email: str, password: str) -> UserDTO | None:
        self._validate_email_exists(email=email)
        user_data = self.user_storage.get_user_details(email=email)
        if not user_data:
            raise NotExistedEmailFound(email=email)

        if user_data.password == password:
            return user_data

        raise WrongPasswordFound(password=password)

    def _validate_username_not_taken(self, username: str):
        is_existed_user_name = self.user_storage.check_username_exists(
            username=username)

        if is_existed_user_name:
            raise ExistedUsernameFound(username=username)

    def _validate_email_not_registered(self, email: str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if is_existed_email:
            raise ExistedEmailFound(email=email)

    def _validate_phone_number_not_exists(self, phone_number: str):
        is_existed_phone_number = self.user_storage.check_phone_number_exists(
            phone_number=phone_number)

        if is_existed_phone_number:
            raise ExistedPhoneNumberFound(phone_number=phone_number)

    def _validate_username_exists(self, username: str):
        is_existed_username = self.user_storage.check_username_exists(
            username=username)

        if not is_existed_username:
            raise UsernameNotFound(username=username)

    def _validate_email_exists(self, email: str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if not is_existed_email:
            raise ExistedEmailFound(email=email)

    def _validate_updated_username_unique(self, username: str, user_id: str):
        is_user_exist_username = self.user_storage.check_user_username_exists(
            user_id=user_id, username=username)

        if not is_user_exist_username:
            self._validate_username_not_taken(username=username)

    def _validate_updated_email_unique(self, user_id: str, email: str):
        is_user_exist_email = self.user_storage.check_user_email_exists(
            user_id=user_id, email=email)

        if not is_user_exist_email:
            self._validate_email_not_registered(email=email)

    def _validate_updated_phone_number_unique(self, user_id: str,
                                               phone_number: str):
        is_user_exist_phone_number = self.user_storage.check_user_phone_number_exists(
            user_id=user_id, phone_number=phone_number)

        if not is_user_exist_phone_number:
            self._validate_phone_number_not_exists(phone_number=phone_number)