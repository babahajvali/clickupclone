from abc import ABC, abstractmethod

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserListPermissionDTO, \
    CreateUserListPermissionDTO


class ListPermissionStorageInterface(ABC):

    @abstractmethod
    def update_user_permission_for_list(self, list_id: str, user_id: str,
                                        permission_type: PermissionsEnum) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def get_list_permissions(self, list_id: str) -> list[
        UserListPermissionDTO]:
        pass

    @abstractmethod
    def get_user_permission_for_list(self, user_id: str,
                                     list_id: str) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def add_user_permission_for_list(self, list_id: str, user_id: str,
                                     permission_type: PermissionsEnum) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def remove_user_permission_for_list(self, list_id: str,
                                        user_id: str) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def create_list_users_permissions(self, user_permissions: list[
        CreateUserListPermissionDTO]) -> list[UserListPermissionDTO]:
        pass
