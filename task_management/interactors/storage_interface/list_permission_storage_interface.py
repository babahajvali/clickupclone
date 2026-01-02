from abc import ABC, abstractmethod

from task_management.exceptions.enums import PermissionsEnum


class ListPermissionStorageInterface(ABC):

    @abstractmethod
    def update_user_permission_for_list(self, list_id: str, user_id: str,
                                        permission_type: PermissionsEnum):
        """Update user permission for a specific list"""
        pass

    @abstractmethod
    def get_list_permissions(self, list_id: str) -> list:
        """Get all permissions for a list"""
        pass

    @abstractmethod
    def get_user_permission_for_list(self, user_id: str, list_id: str):
        """Get user permission for a list"""
        pass

    @abstractmethod
    def add_user_permission_for_list(self, list_id: str, user_id: str,
                                     permission_type: PermissionsEnum):
        """Add new user permission for a list"""
        pass

    @abstractmethod
    def remove_user_permission_for_list(self, list_id: str, user_id: str):
        """Remove user permission from a list"""
        pass