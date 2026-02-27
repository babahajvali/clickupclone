from task_management.exceptions.custom_exceptions import \
    FolderNotFound, DeletedFolderException
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface


class FolderValidationMixin:

    def __init__(self, folder_storage: FolderStorageInterface):
        self.folder_storage = folder_storage

    def check_folder_not_deleted(self, folder_id: str):
        folder_data = self.validate_folder_exists(folder_id=folder_id)

        is_folder_delete = folder_data.is_deleted
        if is_folder_delete:
            raise DeletedFolderException(folder_id=folder_id)

    def validate_folder_exists(self, folder_id: str) -> FolderDTO:

        folder_data = self.folder_storage.get_folder(
            folder_id=folder_id)

        is_folder_not_found = not folder_data
        if is_folder_not_found:
            raise FolderNotFound(folder_id=folder_id)

        return folder_data
