from typing import Optional

from task_management.exceptions.custom_exceptions import ListNotFoundException, \
    InactiveListException, UnexpectedPermissionException, \
    UserListPermissionNotFoundException, InactiveUserListPermissionException, \
    EmptyNameException, UserHaveAlreadyListPermissionException
from task_management.exceptions.enums import Permissions
from task_management.interactors.storage_interfaces import ListStorageInterface


class ListValidationMixin:

    def __init__(self, list_storage: ListStorageInterface, **kwargs):
        self.list_storage = list_storage
        super().__init__(**kwargs)

    def validate_list_is_active(self, list_id: str):
        list_data = self.list_storage.get_list(list_id=list_id)

        is_list_not_found = not list_data
        if is_list_not_found:
            raise ListNotFoundException(list_id=list_id)

        is_list_inactive = not list_data.is_active
        if is_list_inactive:
            raise InactiveListException(list_id=list_id)

    @staticmethod
    def check_permission(permission: str):

        existed_permissions = Permissions.get_values()
        is_permission_invalid = permission not in existed_permissions

        if is_permission_invalid:
            raise UnexpectedPermissionException(permission=permission)

    def check_user_list_permission(self, user_id: str, list_id: str):
        user_permission_data = self.list_storage.get_user_permission_for_list(
            list_id=list_id, user_id=user_id)

        is_user_permission_not_found = not user_permission_data
        if is_user_permission_not_found:
            raise UserListPermissionNotFoundException(list_id=list_id,
                                                      user_id=user_id)

        is_user_permission_inactive = not user_permission_data.is_active
        if is_user_permission_inactive:
            raise InactiveUserListPermissionException(user_id=user_id)

    @staticmethod
    def check_list_name_not_empty(list_name: str):
        is_name_empty = not list_name or not list_name.strip()

        if is_name_empty:
            raise EmptyNameException(name=list_name)

    def get_list_order(self, folder_id: Optional[str], space_id: str) -> int:

        is_folder_provided = folder_id is not None
        if is_folder_provided:
            order = self.list_storage.get_active_lists_last_order_in_folder(
                folder_id=folder_id)
        else:
            order = self.list_storage.get_active_lists_last_order_in_space(
                space_id=space_id)

        return order

    def check_user_have_already_list_permission(self, list_id: str,
                                                user_id: str):

        user_list_permission = self.list_storage.get_user_permission_for_list(
            list_id=list_id, user_id=user_id)

        if user_list_permission:
            is_user_permission_inactive = user_list_permission.is_active
            if is_user_permission_inactive:
                raise UserHaveAlreadyListPermissionException(user_id=user_id)