from typing import Optional

from task_management.exceptions.custom_exceptions import (
    NothingToUpdateList,
    EmptyListName,
    UserHaveAlreadyListPermission,
    UnexpectedPermission,
)
from task_management.exceptions.enums import Permissions
from task_management.interactors.storage_interfaces import ListStorageInterface


class ListValidator:

    def __init__(self, list_storage: ListStorageInterface):
        self.list_storage = list_storage

    def check_update_field_properties(
            self, list_id: str, name: Optional[str], description: Optional[str]
    ) -> dict:

        field_properties_to_update = {}

        is_name_provided = name is not None
        if is_name_provided:
            self.check_list_name_not_empty(list_name=name)
            field_properties_to_update["name"] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update["description"] = description

        if not field_properties_to_update:
            raise NothingToUpdateList(list_id=list_id)

        return field_properties_to_update

    @staticmethod
    def check_list_name_not_empty(list_name: str):
        is_name_empty = not list_name or not list_name.strip()

        if is_name_empty:
            raise EmptyListName(list_name=list_name)

    def check_user_have_already_list_permission(self, list_id: str,
                                                user_id: str):

        user_list_permission = self.list_storage.get_user_permission_for_list(
            list_id=list_id, user_id=user_id
        )

        if not user_list_permission:
            return
        is_user_permission_inactive = user_list_permission.is_active
        if is_user_permission_inactive:
            raise UserHaveAlreadyListPermission(user_id=user_id)

    @staticmethod
    def check_permission(permission: str):

        existed_permissions = Permissions.get_values()
        is_permission_invalid = permission not in existed_permissions

        if is_permission_invalid:
            raise UnexpectedPermission(permission=permission)

    def reorder_list_positions_in_folder(
            self, folder_id: str, old_order: int, new_order: int
    ):

        if new_order > old_order:
            self.list_storage.shift_lists_down_in_folder(
                folder_id=folder_id, old_order=old_order, new_order=new_order
            )
        else:
            self.list_storage.shift_lists_up_in_folder(
                folder_id=folder_id, old_order=old_order, new_order=new_order
            )

    def reorder_list_positions_in_space(
            self, space_id: str, old_order: int, new_order: int
    ):

        if new_order > old_order:
            self.list_storage.shift_lists_down_in_space(
                space_id=space_id, old_order=old_order, new_order=new_order
            )
        else:
            self.list_storage.shift_lists_up_in_space(
                space_id=space_id, old_order=old_order, new_order=new_order
            )
