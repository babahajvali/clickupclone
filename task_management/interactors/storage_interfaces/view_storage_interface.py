from abc import ABC, abstractmethod

from task_management.interactors.dtos import ListViewDTO, CreateListViewDTO


class ViewStorageInterface(ABC):

    @abstractmethod
    def create_list_view(
            self, create_list_view_dto: CreateListViewDTO) -> ListViewDTO:
        pass

    @abstractmethod
    def remove_list_view(self, list_view_id: int) -> ListViewDTO:
        # set the is_active is false
        pass

    @abstractmethod
    def get_list_views(self, list_id: str) -> list[ListViewDTO]:
        # get the active list_view only
        pass

    @abstractmethod
    def is_list_view_exist(self, list_view_id: int) -> bool:
        pass

    @abstractmethod
    def get_list_view(self, list_id: str, view_type: str) -> ListViewDTO:
        pass

    @abstractmethod
    def get_list_view_by_id(self, list_view_id: int) -> ListViewDTO:
        pass

    @abstractmethod
    def update_list_view(
            self, list_view_id: int, view_name: str) -> ListViewDTO:
        pass
