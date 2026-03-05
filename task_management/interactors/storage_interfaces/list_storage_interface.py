from abc import ABC, abstractmethod
from typing import Optional

from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO, CreateListDTO, \
    UserListPermissionDTO, CreateListPermissionDTO


class ListStorageInterface(ABC):

    @abstractmethod
    def get_template_id_by_list_id(self, list_id: str) -> str:
        pass

    @abstractmethod
    def get_list(self, list_id: str) -> ListDTO:
        pass

    @abstractmethod
    def create_list(self, list_data: CreateListDTO, order: int) -> ListDTO:
        pass

    @abstractmethod
    def get_last_list_order(
            self, entity_type: ListEntityType | str, entity_id: str) -> int:
        pass

    @abstractmethod
    def get_workspace_id_by_list_id(self, list_id: str) -> str:
        pass

    @abstractmethod
    def update_list(
            self, list_id: str, name: Optional[str],
            description: Optional[str]) -> ListDTO:
        pass

    @abstractmethod
    def get_folder_lists(self, folder_ids: list[str]) -> list[ListDTO]:
        pass

    @abstractmethod
    def get_space_lists(self, space_ids: list[str]) -> list[ListDTO]:
        pass

    @abstractmethod
    def delete_list(self, list_id: str) -> ListDTO:
        # update the is_active false
        pass

    @abstractmethod
    def update_list_visibility(self, list_id: str, visibility: str) -> ListDTO:
        # set is_private false
        pass

    @abstractmethod
    def update_list_order_in_folder(self, folder_id: str, list_id: str,
                                    order: int) -> ListDTO:
        pass

    @abstractmethod
    def shift_lists_down_in_folder(
            self, folder_id: str, old_order: int, new_order: int):
        pass

    @abstractmethod
    def shift_lists_up_in_folder(
            self, folder_id: str, old_order: int, new_order: int):
        pass

    @abstractmethod
    def update_list_order_in_space(
            self, space_id: str, list_id: str, order: int) -> ListDTO:
        pass

    @abstractmethod
    def shift_lists_down_in_space(
            self, space_id: str, old_order: int, new_order: int):
        pass

    @abstractmethod
    def shift_lists_up_in_space(
            self, space_id: str, old_order: int, new_order: int):
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
    def get_user_permission_for_list(
            self, user_id: str, list_id: str) -> UserListPermissionDTO:
        pass

    @abstractmethod
    def create_list_users_permission(
            self, user_permissions: list[CreateListPermissionDTO]) \
            -> list[UserListPermissionDTO]:
        pass
