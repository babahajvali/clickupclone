from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    UserNotWorkspaceMember, ModificationNotAllowed, WorkspaceMemberNotFound, \
    InactiveWorkspaceMember
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    UserValidationMixin


@invalidate_interactor_cache(cache_name="validate_permission")
class ChangeWorkspaceMemberRoleInteractor(
    WorkspaceValidationMixin,
    UserValidationMixin):

    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
            user_storage: UserStorageInterface):
        super().__init__(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
        )
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    @invalidate_interactor_cache(cache_name='validate_permission')
    def change_workspace_member_role(
            self, workspace_id: str, user_id: str, role: Role,
            changed_by: str) -> WorkspaceMemberDTO:
        self._validate_change_member_role_request(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
            changed_by=changed_by,
        )

        return self.workspace_storage.update_the_member_role(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role.value,
        )

    def _validate_change_member_role_request(
            self, workspace_id: str, user_id: str, role: Role,
            changed_by: str) -> None:
        self.check_role(role=role.value)
        self.check_user_is_active(user_id=user_id)
        self.check_workspace_not_deleted(workspace_id=workspace_id)
        self._check_workspace_member_is_active(
            workspace_id=workspace_id,
            user_id=user_id,
        )
        self._check_user_permission_for_change_workspace_role(
            workspace_id=workspace_id,
            user_id=changed_by,
        )

    def _check_user_permission_for_change_workspace_role(
            self, workspace_id: str, user_id: str) -> None:

        workspace_member_data = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)

        if not workspace_member_data:
            raise UserNotWorkspaceMember(user_id=user_id)

        user_role = workspace_member_data.role
        is_role_restricted = user_role in (Role.MEMBER, Role.GUEST)

        if is_role_restricted:
            raise ModificationNotAllowed(user_id=user_id)

    def _check_workspace_member_is_active(
            self, workspace_id: str, user_id: str) -> None:

        workspace_member_data = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)

        if not workspace_member_data:
            raise WorkspaceMemberNotFound(
                workspace_id=workspace_id, user_id=user_id)

        is_member_inactive = not workspace_member_data.is_active
        if is_member_inactive:
            raise InactiveWorkspaceMember(
                workspace_member_id=workspace_member_data.id)
