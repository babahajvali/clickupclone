from abc import ABC, abstractmethod


class ListStorageInterface(ABC):

    @abstractmethod
    def check_list_exist(self,list_id: str) -> bool:
        pass