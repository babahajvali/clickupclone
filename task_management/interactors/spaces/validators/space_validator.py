from typing import Optional

from task_management.exceptions.custom_exceptions import InvalidOrder, \
    UnexpectedPermission, EmptyName, UnsupportedVisibilityType, \
    NothingToUpdateSpace
from task_management.exceptions.enums import Permissions, Visibility
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface


class SpaceValidator:

    def __init__(self, space_storage: SpaceStorageInterface):
        self.space_storage = space_storage

    def check_space_order(self, workspace_id: str, order: int):

        if order < 1:
            raise InvalidOrder(order=order)
        space_count = self.space_storage.get_workspace_spaces_count(
            workspace_id=workspace_id)

        if order > space_count:
            raise InvalidOrder(order=order)

    @staticmethod
    def check_permission(permission: str):

        existed_permissions = Permissions.get_values()
        is_permission_invalid = permission not in existed_permissions

        if is_permission_invalid:
            raise UnexpectedPermission(permission=permission)

    @staticmethod
    def check_space_name_not_empty(name: str):

        is_name_empty = not name or not name.strip()
        if is_name_empty:
            raise EmptyName(name=name)

    @staticmethod
    def check_visibility_type(visibility: str):

        existed_visibilities = [each.value for each in Visibility]

        is_visibility_invalid = visibility not in existed_visibilities
        if is_visibility_invalid:
            raise UnsupportedVisibilityType(
                visibility_type=visibility)

    def check_space_update_field_properties(
            self, space_id: str, name: Optional[str],
            description: Optional[str]) -> dict:

        field_properties_to_update = {}

        is_name_provided = name is not None
        if is_name_provided:
            self.check_space_name_not_empty(name=name)
            field_properties_to_update['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateSpace(space_id=space_id)

        return field_properties_to_update
