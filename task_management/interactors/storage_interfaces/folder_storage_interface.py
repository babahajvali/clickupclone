from abc import ABC, abstractmethod
from typing import Optional

from task_management.interactors.dtos import FolderDTO, CreateFolderDTO, \
    UserFolderPermissionDTO, CreateFolderPermissionDTO


class FolderStorageInterface(ABC):

    @abstractmethod
    def get_folder(self, folder_id: str) -> FolderDTO:
        pass

    @abstractmethod
    def create_folder(
            self, create_folder_data: CreateFolderDTO,
            order: int) -> FolderDTO:
        pass

    @abstractmethod
    def get_last_folder_order_in_space(self, space_id: str) -> int:
        pass

    @abstractmethod
    def update_folder(
            self, folder_id: str, name: Optional[str],
            description: Optional[str]) -> FolderDTO:
        pass

    @abstractmethod
    def update_folder_order(self, folder_id: str, new_order: int) -> FolderDTO:
        pass

    @abstractmethod
    def shift_folders_down(
            self, space_id: str, old_order: int, new_order: int):
        pass

    @abstractmethod
    def shift_folders_up(self, space_id: str, old_order: int, new_order: int):
        pass

    @abstractmethod
    def delete_folder(self, folder_id: str) -> FolderDTO:
        pass

    @abstractmethod
    def get_workspace_id_from_folder_id(self, folder_id: str) -> str:
        pass

    @abstractmethod
    def get_space_folders(self, space_ids: list[str]) -> list[FolderDTO]:
        # get the spaces active folders
        pass

    @abstractmethod
    def update_folder_visibility(
            self, folder_id: str, visibility: str) -> FolderDTO:
        pass

    @abstractmethod
    def get_space_folder_count(self, space_id: str) -> int:
        # get the active folder count in spaces
        pass

    @abstractmethod
    def get_folder_space_id(self, folder_id: str) -> str:
        pass

    @abstractmethod
    def create_folder_users_permissions(
            self, users_permission_data: list[CreateFolderPermissionDTO]) -> \
            list[UserFolderPermissionDTO]:
        pass
