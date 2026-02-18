from task_management.exceptions.custom_exceptions import UserNotFoundException, \
    InactiveUserException
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class UserValidationMixin:

    def __init__(self, user_storage: UserStorageInterface, **kwargs):
        self.user_storage = user_storage
        super().__init__(**kwargs)

    def validate_user_is_active(self, user_id: str):

        user_data = self.user_storage.get_user_data(user_id=user_id)

        is_user_not_found = not user_data
        if is_user_not_found:
            raise UserNotFoundException(user_id=user_id)

        is_user_inactive = not user_data.is_active
        if is_user_inactive:
            raise InactiveUserException(user_id=user_id)
