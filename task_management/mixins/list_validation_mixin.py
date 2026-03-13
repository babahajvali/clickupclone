from task_management.exceptions.custom_exceptions import ListNotFound, \
    ListIsDeleted, EmptyListName, ModificationNotAllowed, \
    UserNotListMember
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import ListDTO
from task_management.interactors.storage_interfaces import ListStorageInterface


class ListValidationMixin:

    def __init__(self, list_storage: ListStorageInterface, **kwargs):
        self.list_storage = list_storage
        super().__init__(**kwargs)

    def check_list_not_deleted(self, list_id: str):
        list_data = self.check_list_exists(list_id=list_id)

        is_list_deleted = list_data.is_deleted
        if is_list_deleted:
            raise ListIsDeleted(list_id=list_id)

    def check_list_exists(self, list_id: str) -> ListDTO:

        list_data = self.list_storage.get_list(list_id=list_id)

        is_list_not_found = not list_data
        if is_list_not_found:
            raise ListNotFound(list_id=list_id)

        return list_data

    @staticmethod
    def check_list_name_not_empty(list_name: str):
        is_name_empty = not list_name or not list_name.strip()

        if is_name_empty:
            raise EmptyListName(list_name=list_name)

    def check_user_has_edit_access_list_permission(
            self, list_id: str, user_id: str):
        list_permission_dto = self.list_storage.get_user_permission_for_list(
            list_id=list_id,
            user_id=user_id,
        )

        if not list_permission_dto:
            raise UserNotListMember(user_id=user_id, list_id=list_id)

        is_not_full_edit = (
                list_permission_dto.permission_type != PermissionType.FULL_EDIT
        )
        if is_not_full_edit:
            raise ModificationNotAllowed(user_id=user_id)
