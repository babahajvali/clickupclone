from task_management.exceptions.custom_exceptions import \
    SpaceNotFound, DeletedSpaceFound, EmptySpaceName, ModificationNotAllowed, \
    UserNotSpaceMember
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface


class SpaceValidationMixin:

    def __init__(self, space_storage: SpaceStorageInterface, **kwargs):
        self.space_storage = space_storage
        super().__init__(**kwargs)

    def check_space_not_deleted(self, space_id: str):

        space_dto = self.check_space_exists(space_id=space_id)

        is_space_deleted = space_dto.is_deleted
        if is_space_deleted:
            raise DeletedSpaceFound(space_id=space_id)

    def check_space_exists(self, space_id: str) -> SpaceDTO:
        space_dto = self.space_storage.get_space(space_id=space_id)

        if not space_dto:
            raise SpaceNotFound(space_id=space_id)

        return space_dto

    @staticmethod
    def check_space_name_not_empty(name: str):
        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptySpaceName(space_name=name)

    def check_user_has_edit_access_space_permission(
            self, space_id: str, user_id: str):
        space_permission_dto = self.space_storage.get_user_space_permission(
            space_id=space_id, user_id=user_id)

        if not space_permission_dto:
            raise UserNotSpaceMember(user_id=user_id, space_id=space_id)

        is_not_full_edit = \
            (space_permission_dto.permission_type != PermissionType.FULL_EDIT)
        if is_not_full_edit:
            raise ModificationNotAllowed(user_id=user_id)
