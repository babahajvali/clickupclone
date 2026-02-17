from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateViewDTO, ViewDTO, \
    UpdateViewDTO, ListViewDTO


class ViewStorageInterface(ABC):

    @abstractmethod
    def get_all_views(self) -> list[ViewDTO]:
        pass

    @abstractmethod
    def get_view(self, view_id: str) -> ViewDTO:
        pass

    @abstractmethod
    def create_view(self, create_view_data: CreateViewDTO) -> ViewDTO:
        pass

    @abstractmethod
    def update_view(self, view_id: str, update_fields: dict) -> ViewDTO:
        pass

    @abstractmethod
    def check_view_exists(self, view_id: str) -> bool:
        pass

    @abstractmethod
    def apply_view_for_list(self, list_id: str, view_id: str,
                            user_id: str) -> ListViewDTO:
        pass

    @abstractmethod
    def remove_list_view(self, view_id: str, list_id: str, ):
        # set the is_active is false
        pass

    @abstractmethod
    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        # get the active list_view only
        pass

    @abstractmethod
    def is_list_view_exist(self, list_id: str, view_id: str) -> bool:
        pass

    @abstractmethod
    def get_list_view(self, list_id: str, view_id: str) -> ListViewDTO:
        pass
