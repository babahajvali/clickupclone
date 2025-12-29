from abc import ABC, abstractmethod


class UserStorageInterface(ABC):

    @abstractmethod
    def check_user_exist(self,user_id: str) -> bool:
        pass
