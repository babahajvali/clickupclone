from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    ListStorageInterface,
)
from task_management.mixins import FolderValidationMixin


class GetFolderListsInteractor:

    def __init__(
            self,
            list_storage: ListStorageInterface,
            folder_storage: FolderStorageInterface,
    ):
        self.list_storage = list_storage
        self.folder_storage = folder_storage

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @interactor_cache(timeout=5 * 60, cache_name="folder_lists")
    def get_folder_lists(self, folder_id: str):
        self.folder_mixin.check_folder_is_not_deleted(folder_id=folder_id)

        return self.list_storage.get_folder_lists(folder_ids=[folder_id])
