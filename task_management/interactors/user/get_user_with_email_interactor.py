from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface


class GetUserWithEmailInteractor:

    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def get_user_with_email(self, email: str) -> UserDTO | None:
        return self.user_storage.get_user_by_email(email=email)
