from task_management.exceptions.custom_exceptions import \
    UserHaveAlreadyListPermission, UnexpectedPermission
from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import (
    CreateListPermissionDTO,
    UserListPermissionDTO,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.mixins import (
    ListValidationMixin,
    WorkspaceValidationMixin,
)


class AddListPermissionForUserInteractor:

    def __init__(
            self,
            list_storage: ListStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
    ):
        self.list_storage = list_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    def add_user_in_list_permission(
            self, user_permission_data: CreateListPermissionDTO
    ) -> UserListPermissionDTO:
        self._check_user_have_already_list_permission(
            user_id=user_permission_data.user_id,
            list_id=user_permission_data.list_id,
        )
        self.list_mixin.check_list_not_deleted(
            list_id=user_permission_data.list_id)
        self._check_user_has_edit_access_for_list(
            list_id=user_permission_data.list_id,
            user_id=user_permission_data.added_by,
        )
        self._check_permission(
            permission=user_permission_data.permission_type.value
        )

        return self.list_storage.create_list_users_permission(
            user_permissions=[user_permission_data]
        )[0]

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )

    def _check_user_have_already_list_permission(
            self, list_id: str, user_id: str):

        user_list_permission = self.list_storage.get_user_permission_for_list(
            list_id=list_id, user_id=user_id
        )

        if not user_list_permission:
            return
        is_user_permission_inactive = user_list_permission.is_active
        if is_user_permission_inactive:
            raise UserHaveAlreadyListPermission(user_id=user_id)

    @staticmethod
    def _check_permission(permission: str):

        existed_permissions = Permissions.get_values()
        is_permission_invalid = permission not in existed_permissions

        if is_permission_invalid:
            raise UnexpectedPermission(permission=permission)
