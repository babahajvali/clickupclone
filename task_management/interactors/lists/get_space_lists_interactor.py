from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    SpaceStorageInterface,
)
from task_management.mixins import SpaceValidationMixin


class GetSpaceListsInteractor:

    def __init__(
            self,
            list_storage: ListStorageInterface,
            space_storage: SpaceStorageInterface,
    ):
        self.list_storage = list_storage
        self.space_storage = space_storage

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @interactor_cache(timeout=30 * 60, cache_name="space_lists")
    def get_space_lists(self, space_id: str):
        self.space_mixin.check_space_not_deleted(space_id=space_id)

        return self.list_storage.get_space_lists(space_ids=[space_id])
