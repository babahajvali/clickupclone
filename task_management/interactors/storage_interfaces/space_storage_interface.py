from abc import ABC, abstractmethod

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    UpdateSpaceDTO, UserSpacePermissionDTO, CreateUserSpacePermissionDTO


class SpaceStorageInterface(ABC):

    @abstractmethod
    def get_space(self, space_id: str):
        pass

    @abstractmethod
    def create_space(self, create_space_data: CreateSpaceDTO) -> SpaceDTO:
        pass

    @abstractmethod
    def update_space(self, space_id: str, update_fields: dict) -> SpaceDTO:
        pass

    @abstractmethod
    def delete_space(self, space_id: str):
        # set the space is_active is false
        pass

    @abstractmethod
    def set_space_private(self, space_id: str) -> SpaceDTO:
        pass

    @abstractmethod
    def set_space_public(self, space_id: str) -> SpaceDTO:
        pass

    @abstractmethod
    def get_active_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
        pass

    @abstractmethod
    def get_workspace_spaces_count(self, workspace_id: str) -> int:
        # get the active spaces count in workspace
        pass

    @abstractmethod
    def reorder_space(self, workspace_id: str, space_id: str,
                      new_order: int) -> SpaceDTO:
        # get the space order and provided order to reorder spaces
        pass

    @abstractmethod
    def get_space_workspace_id(self, space_id: str) -> str:
        pass

    @abstractmethod
    def get_user_permission_for_space(self, user_id: str,
                                      space_id: str) -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def update_user_permission_for_space(self, user_id: str, space_id: str,
                                         permission_type: Permissions) -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def remove_user_permission_for_space(self, user_id: str,
                                         space_id: str) -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def get_space_permissions(self, space_id: str) -> list[
        UserSpacePermissionDTO]:
        pass

    @abstractmethod
    def create_user_space_permissions(self, permission_data: list[
        CreateUserSpacePermissionDTO]) -> list[UserSpacePermissionDTO]:
        pass

    @abstractmethod
    def check_space_exists(self, space_id: str) -> bool:
        pass
