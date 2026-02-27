from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin


class GetSpaceInteractor:

    def __init__(self, space_storage: SpaceStorageInterface):
        self.space_storage = space_storage

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    def get_space(self, space_id: str) -> SpaceDTO:
        self.space_mixin.validate_space_exists(space_id=space_id)

        return self.space_storage.get_space(space_id=space_id)
