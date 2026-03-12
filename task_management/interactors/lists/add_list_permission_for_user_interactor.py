from task_management.exceptions.custom_exceptions import \
    UserHaveAlreadyListPermission, UnexpectedPermission
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import (
    CreateListPermissionDTO,
    UserListPermissionDTO,
)
from task_management.interactors.storage_interfaces import ListStorageInterface
from task_management.mixins import (
    ListValidationMixin,
)


class AddListPermissionForUserInteractor(ListValidationMixin):

    def __init__(
            self, list_storage: ListStorageInterface):
        super().__init__(list_storage=list_storage)
        self.list_storage = list_storage

    def add_user_in_list_permission(
            self, user_permission_dto: CreateListPermissionDTO) \
            -> UserListPermissionDTO:
        self._check_user_have_already_list_permission(
            user_id=user_permission_dto.user_id,
            list_id=user_permission_dto.list_id,
        )
        self.check_list_not_deleted(
            list_id=user_permission_dto.list_id)
        self.check_user_has_edit_access_list_permission(
            list_id=user_permission_dto.list_id,
            user_id=user_permission_dto.added_by,
        )
        self._check_permission(
            permission=user_permission_dto.permission_type.value
        )

        return self.list_storage.create_list_users_permission(
            user_permissions=[user_permission_dto])[0]

    def _check_user_have_already_list_permission(
            self, list_id: str, user_id: str):

        user_list_permission = self.list_storage.get_user_permission_for_list(
            list_id=list_id, user_id=user_id
        )

        if not user_list_permission:
            return
        is_user_permission_active = user_list_permission.is_active
        if is_user_permission_active:
            raise UserHaveAlreadyListPermission(user_id=user_id)

    @staticmethod
    def _check_permission(permission: str):

        existed_permissions = PermissionType.get_values()
        is_permission_invalid = permission not in existed_permissions

        if is_permission_invalid:
            raise UnexpectedPermission(permission=permission)
