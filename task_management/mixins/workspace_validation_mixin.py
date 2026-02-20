from task_management.exceptions.custom_exceptions import \
    InactiveWorkspace, ModificationNotAllowed, \
    UserNotWorkspaceOwner, WorkspaceNotFound, \
    InactiveWorkspaceMember, UserNotWorkspaceMember, \
    WorkspaceMemberIdNotFound
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface


class WorkspaceValidationMixin:
    def __init__(self, workspace_storage: WorkspaceStorageInterface, **kwargs):
        self.workspace_storage = workspace_storage
        super().__init__(**kwargs)

    def check_workspace_is_active(self, workspace_id: str):
        workspace_data = self.workspace_storage.get_workspace(
            workspace_id=workspace_id)

        if not workspace_data:
            raise WorkspaceNotFound(workspace_id=workspace_id)

        if not workspace_data.is_active:
            raise InactiveWorkspace(workspace_id=workspace_id)

    def check_user_is_workspace_owner(self, user_id: str,
                                      workspace_id: str):
        is_owner = self.workspace_storage.validate_user_is_workspace_owner(
            workspace_id=workspace_id, user_id=user_id)

        if not is_owner:
            raise UserNotWorkspaceOwner(user_id=user_id)

    def check_user_has_access_to_workspace(
            self, user_id: str, workspace_id: str):

        member_permission = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id,
            user_id=user_id
        )
        is_member_not_found = not member_permission
        is_user_not_allowed = member_permission.role == Role.GUEST

        if is_member_not_found:
            raise UserNotWorkspaceMember(user_id=user_id)

        if is_user_not_allowed:
            raise ModificationNotAllowed(user_id=user_id)

    def check_workspace_member_is_active(self, workspace_member_id: int):
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

        is_member_not_found = not workspace_member_data

        if is_member_not_found:
            raise WorkspaceMemberIdNotFound(
                workspace_member_id=workspace_member_id)

        if not workspace_member_data.is_active:
            raise InactiveWorkspaceMember(
                workspace_member_id=workspace_member_id)

    def check_user_permission_for_change_workspace_role(
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
