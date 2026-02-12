from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateViewDTO, ViewDTO, \
    UpdateViewDTO


class ViewStorageInterface(ABC):

    @abstractmethod
    def get_all_views(self) -> list[ViewDTO]:
        pass

    @abstractmethod
    def get_view(self,view_id: str) -> ViewDTO:
        pass

    @abstractmethod
    def create_view(self,create_view_data: CreateViewDTO) -> ViewDTO:
        pass

    @abstractmethod
    def update_view(self,update_view_data: UpdateViewDTO) -> ViewDTO:
        pass

    @abstractmethod
    def check_view_exists(self,view_id: str) -> bool:
        pass
