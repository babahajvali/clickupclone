from task_management.exceptions.custom_exceptions import \
    SpaceNotFound, DeletedSpaceFound
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface


class SpaceValidationMixin:

    def __init__(self, space_storage: SpaceStorageInterface):
        self.space_storage = space_storage

    def check_space_not_deleted(self, space_id: str):

        space_data = self.validate_space_exists(space_id=space_id)

        is_space_delete = space_data.is_deleted
        if is_space_delete:
            raise DeletedSpaceFound(space_id=space_id)

    def validate_space_exists(self, space_id: str) -> SpaceDTO:
        space_data = self.space_storage.get_space(space_id=space_id)

        is_space_not_found = not space_data
        if is_space_not_found:
            raise SpaceNotFound(space_id=space_id)

        return space_data
