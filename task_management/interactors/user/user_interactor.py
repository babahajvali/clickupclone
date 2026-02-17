from task_management.exceptions.custom_exceptions import \
    EmailNotFoundException, IncorrectPasswordException, \
    UsernameAlreadyExistsException, EmailAlreadyExistsException,\
    PhoneNumberAlreadyExistsException, InactiveUserException
from task_management.interactors.dtos import CreateUserDTO, UserDTO, \
    UpdateUserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.mixins import UserValidationMixin


class UserInteractor(UserValidationMixin):
    def __init__(self, user_storage: UserStorageInterface):
        super().__init__(user_storage=user_storage)
        self.user_storage = user_storage

    def create_user(self, user_details: CreateUserDTO) -> UserDTO:

        self._is_username_taken(user_details.username)
        self._is_email_registered(email=user_details.email)
        self._is_phone_number_exists(phone_number=user_details.phone_number)

        return self.user_storage.create_user(user_data=user_details)

    def update_user(self, user_update_data: UpdateUserDTO) -> UserDTO:

        user_id = user_update_data.user_id
        self.validate_user_is_active(user_id=user_id)
        is_username_provided = user_update_data.username is not None
        is_email_provided = user_update_data.email is not None
        is_phone_number_provided = user_update_data.phone_number is not None

        if is_username_provided:
            self._check_username_except_current_user(
                username=user_update_data.username, user_id=user_id)
        if is_email_provided:
            self._check_email_except_current_user(email=user_update_data.email,
                                                  user_id=user_id)
        if is_phone_number_provided:
            self._check_phone_number_except_current_user(
                user_id=user_id, phone_number=user_update_data.phone_number)

        return self.user_storage.update_user(user_data=user_update_data)

    def get_user_profile(self, user_id: str) -> UserDTO:

        self.validate_user_is_active(user_id=user_id)

        return self.user_storage.get_user_data(user_id=user_id)

    def block_user(self, user_id: str) -> UserDTO:

        self.validate_user_is_active(user_id=user_id)

        return self.user_storage.block_user(user_id=user_id)

    def user_login(self, email: str, password: str) -> UserDTO:

        is_email_exist = self.user_storage.check_email_exists(email=email)

        if not is_email_exist:
            raise EmailNotFoundException(email=email)
        user_data = self.user_storage.get_user_details(email=email)

        if not user_data.is_active:
            raise InactiveUserException(user_id=user_data.user_id)

        if user_data.password == password:
            return user_data

        raise IncorrectPasswordException(password=password)

    def _is_username_taken(self, username: str):
        is_existed_username = self.user_storage.check_username_exists(
            username=username)

        if is_existed_username:
            raise UsernameAlreadyExistsException(username=username)

    def _is_email_registered(self, email: str):
        is_existed_email = self.user_storage.check_email_exists(email=email)

        if is_existed_email:
            raise EmailAlreadyExistsException(email=email)

    def _is_phone_number_exists(self, phone_number: str):
        is_existed_phone_number = self.user_storage.check_phone_number_exists(
            phone_number=phone_number)

        if is_existed_phone_number:
            raise PhoneNumberAlreadyExistsException(phone_number=phone_number)

    def _check_username_except_current_user(self, username: str,
                                            user_id: str):
        is_user_exist_username = self.user_storage.check_username_except_current_user(
            user_id=user_id, username=username)

        if is_user_exist_username:
            raise UsernameAlreadyExistsException(username=username)

    def _check_email_except_current_user(self, user_id: str, email: str):

        is_user_exist_email = self.user_storage.check_email_exists_except_current_user(
            user_id=user_id, email=email)

        if is_user_exist_email:
            raise EmailAlreadyExistsException(email=email)

    def _check_phone_number_except_current_user(self, user_id: str,
                                                phone_number: str):

        is_user_exist_phone_number = self.user_storage.check_phone_number_except_current_user(
            user_id=user_id, phone_number=phone_number)

        if is_user_exist_phone_number:
            raise PhoneNumberAlreadyExistsException(phone_number=phone_number)
