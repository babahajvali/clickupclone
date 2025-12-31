from abc import ABC, abstractmethod


class SpaceStorageInterface(ABC):

    @abstractmethod
    def get_space(self, space_id: str):
        pass
