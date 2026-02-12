from abc import ABC, abstractmethod
from typing import Optional

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import ListDTO, CreateListDTO, \
    UpdateListDTO, FieldDTO, UserListPermissionDTO, CreateUserListPermissionDTO


class ListStorageInterface(ABC):

    @abstractmethod
    def get_template_id_by_list_id(self, list_id: str) -> str:
        pass

    @abstractmethod
    def get_list(self, list_id: str) -> ListDTO:
        pass

    @abstractmethod
    def create_list(self, create_list_data: CreateListDTO) -> ListDTO:
        # order is auto-increase in folder or space
        pass

    @abstractmethod
    def update_list(self, list_id: str, update_fields: dict) -> ListDTO:
        pass

    @abstractmethod
    def get_folder_lists(self, folder_ids: list[str]) -> list[ListDTO]:
        pass

    @abstractmethod
    def get_space_lists(self, space_ids: list[str]) -> list[ListDTO]:
        pass

    @abstractmethod
    def remove_list(self, list_id: str) -> ListDTO:
        # update the is_active false
        pass

    @abstractmethod
    def make_list_private(self, list_id: str) -> ListDTO:
        # set the is_private is true
        pass

    @abstractmethod
    def make_list_public(self, list_id: str) -> ListDTO:
        # set is_private false
        pass

    @abstractmethod
    def reorder_list_in_folder(self, folder_id: str, list_id: str,
                               order: int) -> ListDTO:
        pass

    @abstractmethod
    def reorder_list_in_space(self, space_id: str, list_id: str, order: int) -> \
            ListDTO:
        pass

    @abstractmethod
    def get_folder_lists_count(self, folder_id: str) -> int:
        pass

    @abstractmethod
    def get_space_lists_count(self, space_id: str) -> int:
        pass

    @abstractmethod
    def get_list_space_id(self, list_id: str) -> str:
        pass

    @abstractmethod
    def update_user_permission_for_list(self, list_id: str, user_id: str,
                                        permission_type: Permissions) -> UserListPermissionDTO:
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
                                     permission_type: Permissions) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def remove_user_permission_for_list(self, list_id: str,
                                        user_id: str) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def create_list_users_permissions(self, user_permissions: list[
        CreateUserListPermissionDTO]) -> list[UserListPermissionDTO]:
        pass
