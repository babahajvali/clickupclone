from task_management.interactors.dtos import FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface
from task_management.mixins import FolderValidationMixin


class GetFolderInteractor:

    def __init__(self, folder_storage: FolderStorageInterface):
        self.folder_storage = folder_storage

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    def get_folder(self, folder_id: str) -> FolderDTO:
        self.folder_mixin.validate_folder_exists(folder_id=folder_id)

        return self.folder_storage.get_folder(folder_id=folder_id)
