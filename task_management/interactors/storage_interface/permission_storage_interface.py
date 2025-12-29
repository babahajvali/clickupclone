from abc import ABC, abstractmethod


class PermissionStorageInterface(ABC):

    @abstractmethod
    def get_user_access_permissions(self, user_id: str):
        pass