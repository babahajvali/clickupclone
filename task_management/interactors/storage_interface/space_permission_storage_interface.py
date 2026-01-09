from abc import ABC, abstractmethod

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserSpacePermissionDTO, \
    CreateUserSpacePermissionDTO


class SpacePermissionStorageInterface(ABC):

    @abstractmethod
    def get_user_permission_for_space(self,user_id:str, space_id:str) -> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def update_user_permission_for_space(self,user_id: str, space_id:str, permission_type: PermissionsEnum)-> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def remove_user_permission_for_space(self,user_id: str, space_id:str)-> UserSpacePermissionDTO:
        pass

    @abstractmethod
    def get_space_permissions(self,space_id:str) -> list[UserSpacePermissionDTO]:
        pass

    @abstractmethod
    def create_user_space_permissions(self, permission_data: list[CreateUserSpacePermissionDTO]) -> list[UserSpacePermissionDTO]:
        pass