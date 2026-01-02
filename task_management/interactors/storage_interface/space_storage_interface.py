from abc import ABC, abstractmethod

from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO


class SpaceStorageInterface(ABC):

    @abstractmethod
    def get_space(self, space_id: str):
        pass

    @abstractmethod
    def create_space(self,create_space_data: CreateSpaceDTO)-> SpaceDTO:
        pass

    @abstractmethod
    def check_space_order_exist(self,order: int, workspace_id: str):
        pass

    @abstractmethod
    def update_space(self,update_space_data: SpaceDTO)-> SpaceDTO:
        pass

    @abstractmethod
    def remove_space(self,space_id: str,user_id: str):
        #set the space is_active is false
        pass

    @abstractmethod
    def set_space_private(self,space_id: str, user_id: str)-> SpaceDTO:
        pass

    @abstractmethod
    def set_space_public(self,space_id: str, user_id: str)-> SpaceDTO:
        pass

    @abstractmethod
    def get_workspace_spaces(self,workspace_id: str) -> list[SpaceDTO]:
        pass

