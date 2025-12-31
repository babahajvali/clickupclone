from abc import ABC, abstractmethod

class FolderStorageInterface(ABC):

    @abstractmethod
    def get_folder(self, folder_id: str):
        pass
