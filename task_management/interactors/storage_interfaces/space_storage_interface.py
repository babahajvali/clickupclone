from abc import ABC, abstractmethod

from typing import Optional

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    UserSpacePermissionDTO, CreateUserSpacePermissionDTO


class SpaceStorageInterface(ABC):

    @abstractmethod
    def get_space(self, space_id: str):
        pass

    @abstractmethod
    def create_space(
            self, space_data: CreateSpaceDTO, order: int) -> SpaceDTO:
        pass

    @abstractmethod
    def get_last_space_order_in_workspace(self, workspace_id: str) -> int:
        pass

    @abstractmethod
    def update_space(
            self, space_id: str, name: Optional[str],
            description: Optional[str]) -> SpaceDTO:
        pass

    @abstractmethod
    def delete_space(self, space_id: str):
        # set the spaces is_active is false
        pass

    @abstractmethod
    def update_space_visibility(
            self, space_id: str, visibility: str) -> SpaceDTO:
        pass

    @abstractmethod
    def get_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
        pass

    @abstractmethod
    def get_workspace_spaces_count(self, workspace_id: str) -> int:
        pass

    @abstractmethod
    def update_space_order(self, space_id: str, new_order: int) -> SpaceDTO:
        pass

    @abstractmethod
    def shift_spaces_down(
            self, workspace_id: str, current_order: int, new_order: int):
        pass

    @abstractmethod
    def shift_spaces_up(
            self, workspace_id: str, current_order: int, new_order: int):
        pass

    @abstractmethod
    def get_space_workspace_id(self, space_id: str) -> str:
        pass

    @abstractmethod
    def get_user_permission_for_space(
            self, user_id: str, space_id: str) -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def update_user_permission_for_space(
            self, user_id: str, space_id: str, permission_type: Permissions) \
            -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def remove_user_permission_for_space(
            self, user_id: str, space_id: str) -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def get_space_permissions(
            self, space_id: str) -> list[UserSpacePermissionDTO]:
        pass

    @abstractmethod
    def create_user_space_permissions(
            self, permission_data: list[CreateUserSpacePermissionDTO]) \
            -> list[UserSpacePermissionDTO]:
        pass

    @abstractmethod
    def check_space_exists(self, space_id: str) -> bool:
        pass
