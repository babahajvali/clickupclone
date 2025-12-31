from abc import ABC, abstractmethod

from task_management.interactors.dtos import ListDTO, CreateListDTO, \
    UpdateListDTO


class ListStorageInterface(ABC):

    @abstractmethod
    def check_list_exist(self, list_id: str) -> bool:
        pass

    @abstractmethod
    def get_list(self, list_id: str) -> ListDTO:
        pass

    @abstractmethod
    def check_list_order_exist_in_folder(self, order: int,
                                         folder_id: str) -> bool:
        # check this order already exist
        pass

    @abstractmethod
    def check_list_order_exist_in_space(self, order: int,
                                        space_id: str) -> bool:
        # check this order already exist
        pass

    @abstractmethod
    def crate_list(self, create_list_data: CreateListDTO) -> ListDTO:
        pass

    @abstractmethod
    def update_list(self, update_list_data: UpdateListDTO) -> ListDTO:
        pass

    @abstractmethod
    def get_folder_lists(self, folder_id: str) -> list[ListDTO]:
        pass

    @abstractmethod
    def get_space_lists(self, space_id: str) -> list[ListDTO]:
        pass

    @abstractmethod
    def remove_list(self, list_id: str) -> ListDTO:
        # update the is_active false
        pass

    @abstractmethod
    def make_list_private(self, list_id: str) -> ListDTO:
        # set the is_private is true
        pass

    @abstractmethod
    def make_list_public(self, list_id: str) -> ListDTO:
        # set is_private false
        pass
