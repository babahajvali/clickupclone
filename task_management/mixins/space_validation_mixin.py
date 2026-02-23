from task_management.exceptions.custom_exceptions import \
    SpaceNotFound, InactiveSpace
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface


class SpaceValidationMixin:

    def __init__(self, space_storage: SpaceStorageInterface, **kwargs):
        self.space_storage = space_storage
        super().__init__(**kwargs)

    def check_space_is_active(self, space_id: str):

        space_data = self.space_storage.get_space(space_id=space_id)

        is_space_not_found = not space_data
        if is_space_not_found:
            raise SpaceNotFound(space_id=space_id)

        is_space_inactive = not space_data.is_delete
        if is_space_inactive:
            raise InactiveSpace(space_id=space_id)

    def check_space_exists(self, space_id: str):
        is_exist = self.space_storage.check_space_exists(space_id=space_id)

        is_space_not_found = not is_exist
        if is_space_not_found:
            raise SpaceNotFound(space_id=space_id)