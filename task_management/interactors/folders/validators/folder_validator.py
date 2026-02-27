from task_management.exceptions.custom_exceptions import EmptyFolderName
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface


class FolderValidator:

    def __init__(self, folder_storage: FolderStorageInterface):
        self.folder_storage = folder_storage

    @staticmethod
    def check_folder_name_not_empty(name: str):
        is_name_empty = name is None or not name.strip()

        if is_name_empty:
            raise EmptyFolderName(folder_name=name)
