from abc import ABC, abstractmethod


class UserStorageInterface(ABC):

    @abstractmethod
    def check_user_exists(self, user_id: str) -> bool:
        pass
