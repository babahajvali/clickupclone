from abc import ABC, abstractmethod

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import FolderDTO, CreateFolderDTO, \
    UpdateFolderDTO, UserFolderPermissionDTO, CreateFolderPermissionDTO


class FolderStorageInterface(ABC):

    @abstractmethod
    def get_folder(self, folder_id: str) -> FolderDTO:
        pass

    @abstractmethod
    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:
        pass

    @abstractmethod
    def update_folder(self, folder_id: str,
                      field_properties: dict) -> FolderDTO:
        pass

    @abstractmethod
    def reorder_folder(self, folder_id: str, new_order: int) -> FolderDTO:
        pass

    @abstractmethod
    def remove_folder(self, folder_id: str) -> FolderDTO:
        # in this case update the value is_active is  False
        pass

    @abstractmethod
    def get_space_folders(self, space_ids: list[str]) -> list[FolderDTO]:
        # get the spaces active folders
        pass

    @abstractmethod
    def set_folder_private(self, folder_id: str) -> FolderDTO:
        # set the folder to private
        pass

    @abstractmethod
    def set_folder_public(self, folder_id: str) -> FolderDTO:
        # set folder is public
        pass

    @abstractmethod
    def get_space_folder_count(self, space_id: str) -> int:
        # get the active folder count in spaces
        pass

    @abstractmethod
    def get_folder_space_id(self, folder_id: str) -> str:
        pass

    @abstractmethod
    def get_user_permission_for_folder(self, user_id: str,
                                       folder_id: str) -> UserFolderPermissionDTO:
        pass

    @abstractmethod
    def update_user_permission_for_folder(self, user_id: str, folder_id: str,
                                          permission_type: Permissions) -> UserFolderPermissionDTO:
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
                                            CreateFolderPermissionDTO]) -> \
            list[UserFolderPermissionDTO]:
        pass
