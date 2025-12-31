from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateViewDTO, ViewDTO, \
    UpdateViewDTO


class ViewStorageInterface(ABC):

    @abstractmethod
    def chek_view_exist(self,view_id: str) -> bool:
        pass

    @abstractmethod
    def create_view(self,create_view_data: CreateViewDTO) -> ViewDTO:
        pass

    @abstractmethod
    def update_view(self,update_view_data: UpdateViewDTO) -> ViewDTO:
        pass