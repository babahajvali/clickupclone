from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    UserNotWorkspaceMember, ModificationNotAllowed
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator
from task_management.mixins import WorkspaceValidationMixin, \
    UserValidationMixin


class ChangeWorkspaceMemberRoleInteractor:

    def __init__(self,
                 workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    @property
    def workspace_validator(self) -> WorkspaceValidator:
        return WorkspaceValidator(workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    @invalidate_interactor_cache(cache_name='validate_permission')
    def change_member_role(
            self, workspace_id: str, user_id: str, role: str,
            changed_by: str) -> WorkspaceMemberDTO:
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=workspace_id
        )
        self.user_mixin.check_user_is_active(user_id=user_id)
        self.workspace_validator.check_workspace_member_is_active(
            workspace_id=workspace_id, user_id=user_id
        )

        self._check_user_permission_for_change_workspace_role(
            user_id=changed_by, workspace_id=workspace_id)

        self.workspace_validator.check_role(role=role)

        return self.workspace_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=user_id, role=role
        )

    def _check_user_permission_for_change_workspace_role(
            self, workspace_id: str, user_id: str):

        member_permission = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)

        is_member_not_found = not member_permission

        if is_member_not_found:
            raise UserNotWorkspaceMember(user_id=user_id)

        user_role = member_permission.role
        is_user_not_allowed = user_role == Role.MEMBER or user_role == Role.GUEST

        if is_user_not_allowed:
            raise ModificationNotAllowed(user_id=user_id)
