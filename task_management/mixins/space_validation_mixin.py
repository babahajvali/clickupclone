from task_management.exceptions.custom_exceptions import \
    SpaceNotFoundException, InactiveSpaceException
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface


class SpaceValidationMixin:

    def __init__(self, space_storage: SpaceStorageInterface, **kwargs):
        self.space_storage = space_storage
        super().__init__(**kwargs)

    def validate_space_is_active(self, space_id: str):

        space_data = self.space_storage.get_space(space_id=space_id)

        if not space_data:
            raise SpaceNotFoundException(space_id=space_id)

        if not space_data.is_active:
            raise InactiveSpaceException(space_id=space_id)

    def check_space_exists(self, space_id: str):
        is_exist = self.space_storage.check_space_exists(space_id=space_id)

        if not is_exist:
            raise SpaceNotFoundException(space_id=space_id)