from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.mixins import UserValidationMixin


class GetUserProfileInteractor(UserValidationMixin):

    def __init__(self, user_storage: UserStorageInterface):
        super().__init__(user_storage=user_storage)
        self.user_storage = user_storage

    def get_user_profile(self, user_id: str) -> UserDTO:
        self.check_user_is_active(user_id=user_id)

        return self.user_storage.get_user(user_id=user_id)
