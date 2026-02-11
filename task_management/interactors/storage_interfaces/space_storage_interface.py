from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    UpdateSpaceDTO


class SpaceStorageInterface(ABC):

    @abstractmethod
    def get_space(self, space_id: str):
        pass

    @abstractmethod
    def create_space(self,create_space_data: CreateSpaceDTO)-> SpaceDTO:
        pass

    @abstractmethod
    def update_space(self,update_space_data: UpdateSpaceDTO)-> SpaceDTO:
        pass

    @abstractmethod
    def remove_space(self,space_id: str):
        #set the space is_active is false
        pass

    @abstractmethod
    def set_space_private(self,space_id: str)-> SpaceDTO:
        pass

    @abstractmethod
    def set_space_public(self,space_id: str)-> SpaceDTO:
        pass

    @abstractmethod
    def get_workspace_spaces(self,workspace_id: str) -> list[SpaceDTO]:
        pass

    @abstractmethod
    def get_workspace_spaces_count(self,workspace_id: str) -> int:
        # get the active spaces count in workspace
        pass

    @abstractmethod
    def reorder_space(self,workspace_id: str, space_id: str, new_order: int)-> SpaceDTO:
        # get the space order and provided order to reorder spaces
        pass

    @abstractmethod
    def get_space_workspace_id(self,space_id: str) -> str:
        pass

