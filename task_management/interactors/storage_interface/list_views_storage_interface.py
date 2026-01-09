from abc import ABC, abstractmethod

from task_management.interactors.dtos import ListViewDTO, RemoveListViewDTO


class ListViewsStorageInterface(ABC):

    @abstractmethod
    def apply_view_for_list(self, list_id: str, view_id: str,
                            user_id: str) -> ListViewDTO:
        pass

    @abstractmethod
    def remove_view_for_list(self, view_id: str, list_id: str,):
        #set the is_active is false
        pass

    @abstractmethod
    def get_list_views(self,list_id: str) -> list[ListViewDTO]:
        # get the active list_view only
        pass

