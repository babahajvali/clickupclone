from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin


class GetSpaceFoldersInteractor:
    def __init__(
            self, folder_storage: FolderStorageInterface,
            space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.space_storage = space_storage

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @interactor_cache(cache_name="folders", timeout=5 * 60)
    def get_space_folders(self, space_id: str) -> list[FolderDTO]:
        self.space_mixin.check_space_not_deleted(space_id=space_id)

        return self.folder_storage.get_space_folders(
            space_ids=[space_id]
        )
