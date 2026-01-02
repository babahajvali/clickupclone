from abc import ABC, abstractmethod

from task_management.exceptions.enums import PermissionsEnum


class SpacePermissionStorageInterface(ABC):

    @abstractmethod
    def get_user_permission_for_space(self,user_id:str, space_id:str):
        pass

    @abstractmethod
    def add_user_permission_for_space(self,user_id: str, space_id:str, permission_type: PermissionsEnum):
        pass

    @abstractmethod
    def update_user_permission_for_space(self,user_id: str, space_id:str, permission_type: PermissionsEnum):
        pass

    @abstractmethod
    def remove_user_permission_for_space(self,user_id: str, space_id:str):
        pass

    @abstractmethod
    def get_space_permissions(self,space_id:str):
        pass