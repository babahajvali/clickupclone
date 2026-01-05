from abc import ABC, abstractmethod

from task_management.interactors.dtos import FolderDTO, CreateFolderDTO, \
    UpdateFolderDTO


class FolderStorageInterface(ABC):

    @abstractmethod
    def get_folder(self, folder_id: str):
        pass

    @abstractmethod
    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:
        pass

    @abstractmethod
    def update_folder(self,  update_folder_data: UpdateFolderDTO) -> FolderDTO:
        pass

    @abstractmethod
    def reorder_folder(self,folder_id: str, order: int) -> FolderDTO:
        pass

    @abstractmethod
    def remove_folder(self,folder_id: str) -> FolderDTO:
        # in this case update the value is_active is  False
        pass

    @abstractmethod
    def get_space_folders(self, space_ids: list[str]) -> list[FolderDTO]:
        #get the space active folders
        pass

    @abstractmethod
    def check_order_exist(self, order: int, space_id: str) -> bool:
        pass

    @abstractmethod
    def set_folder_private(self,folder_id: str) -> FolderDTO:
        # set the folder to private
        pass


    @abstractmethod
    def set_folder_public(self,folder_id: str) -> FolderDTO:
        #set folder is public
        pass

    @abstractmethod
    def get_space_folder_count(self,space_id: str)-> int:
        # get the active folder count in space
        pass

