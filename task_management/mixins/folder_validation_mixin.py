from task_management.exceptions.custom_exceptions import \
    FolderNotFoundException, InactiveFolderException
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface


class FolderValidationMixin:

    def __init__(self, folder_storage: FolderStorageInterface, ** kwargs):
        self.folder_storage = folder_storage
        super().__init__(**kwargs)

    def validate_folder_is_active(self, folder_id: str):
        folder_data = self.folder_storage.get_folder(folder_id=folder_id)

        if not folder_data:
            raise FolderNotFoundException(folder_id=folder_id)

        if not folder_data.is_active:
            raise InactiveFolderException(folder_id=folder_id)