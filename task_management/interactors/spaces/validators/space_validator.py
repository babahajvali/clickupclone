from task_management.exceptions.custom_exceptions import EmptySpaceName
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface


class SpaceValidator:

    def __init__(self, space_storage: SpaceStorageInterface):
        self.space_storage = space_storage

    @staticmethod
    def check_space_name_not_empty(name: str):
        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptySpaceName(space_name=name)
