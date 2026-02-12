from task_management.exceptions.custom_exceptions import \
    InactiveWorkspaceException, ModificationNotAllowedException, \
    UserNotWorkspaceOwnerException, WorkspaceNotFoundException, \
    InactiveWorkspaceMemberException
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface


class WorkspaceValidationMixin:
    def __init__(self, workspace_storage: WorkspaceStorageInterface, **kwargs):
        self.workspace_storage = workspace_storage
        super().__init__(**kwargs)

    def validate_workspace_is_active(self, workspace_id: str):
        workspace_data = self.workspace_storage.get_workspace(
            workspace_id=workspace_id)

        if not workspace_data:
            raise WorkspaceNotFoundException(workspace_id=workspace_id)

        if not workspace_data.is_active:
            raise InactiveWorkspaceException(workspace_id=workspace_id)

    def validate_user_is_workspace_owner(self, user_id: str,
                                         workspace_id: str):
        is_owner = self.workspace_storage.validate_user_is_workspace_owner(
            workspace_id=workspace_id, user_id=user_id)

        if not is_owner:
            raise UserNotWorkspaceOwnerException(user_id=user_id)

    def validate_user_has_access_to_workspace(
            self, user_id: str, workspace_id: str):

        member_permission = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id,
            user_id=user_id
        )

        if not member_permission or member_permission.role == Role.GUEST:
            raise ModificationNotAllowedException(user_id=user_id)

    def validate_workspace_member_is_active(self, workspace_member_id: int):
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

        if not workspace_member_data.is_active:
            raise InactiveWorkspaceMemberException(
                workspace_member_id=workspace_member_id)

    def validate_user_permission_for_change_workspace_role(
            self, workspace_id: str, user_id: str):

        member_permission = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)
        user_role = member_permission.role

        if not member_permission or (
                user_role == Role.MEMBER or user_role == Role.GUEST):
            raise ModificationNotAllowedException(user_id=user_id)

