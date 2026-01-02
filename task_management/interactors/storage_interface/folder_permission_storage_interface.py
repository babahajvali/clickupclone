from abc import ABC, abstractmethod

from task_management.exceptions.enums import PermissionsEnum


class FolderPermissionStorageInterface(ABC):

    @abstractmethod
    def get_user_permission_for_folder(self,user_id:str, folder_id:str):
        """Get user permission for a folder"""
        pass

    @abstractmethod
    def add_user_permission_for_folder(self,user_id:str, folder_id:str,permission_type: PermissionsEnum):
        pass

    @abstractmethod
    def update_user_permission_for_folder(self, user_id:str, folder_id:str, permission_type: PermissionsEnum):
        pass

    @abstractmethod
    def remove_user_permission_for_folder(self, folder_id:str, user_id:str):
        pass


