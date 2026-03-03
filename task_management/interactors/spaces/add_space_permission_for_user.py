from task_management.exceptions.custom_exceptions import UnexpectedPermission
from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import UserSpacePermissionDTO, \
    CreateUserSpacePermissionDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class AddSpacePermissionForUser:

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    def add_user_for_space_permission(
            self, user_data: CreateUserSpacePermissionDTO) \
            -> UserSpacePermissionDTO:
        self.space_mixin.check_space_not_deleted(
            space_id=user_data.space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=user_data.space_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_data.user_id, workspace_id=workspace_id)
        self._check_permission(
            permission=user_data.permission_type.value)

        return self.space_storage.create_user_space_permissions(
            permission_data=[user_data])[0]

    @staticmethod
    def _check_permission(permission: str):
        existed_permissions = Permissions.get_values()
        is_permission_invalid = permission not in existed_permissions

        if is_permission_invalid:
            raise UnexpectedPermission(permission=permission)
