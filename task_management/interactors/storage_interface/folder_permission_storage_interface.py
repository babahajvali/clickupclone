from abc import ABC, abstractmethod

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserFolderPermissionDTO, \
    CreateUserFolderPermissionDTO


class FolderPermissionStorageInterface(ABC):

    @abstractmethod
    def get_user_permission_for_folder(self, user_id: str,
                                       folder_id: str) -> UserFolderPermissionDTO:
        """Get user permission for a folder"""
        pass

    @abstractmethod
    def add_user_permission_for_folder(self, user_id: str, folder_id: str,
                                       permission_type: PermissionsEnum) -> UserFolderPermissionDTO:
        pass

    @abstractmethod
    def update_user_permission_for_folder(self, user_id: str, folder_id: str,
                                          permission_type: PermissionsEnum) -> UserFolderPermissionDTO:
        pass

    @abstractmethod
    def remove_user_permission_for_folder(self, folder_id: str,
                                          user_id: str) -> UserFolderPermissionDTO:
        pass

    @abstractmethod
    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:
        pass

    @abstractmethod
    def create_folder_users_permissions(self,
                                        users_permission_data: list[
                                            CreateUserFolderPermissionDTO]) -> \
            list[UserFolderPermissionDTO]:
        pass
