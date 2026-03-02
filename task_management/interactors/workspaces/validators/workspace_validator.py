from task_management.exceptions.custom_exceptions import \
    WorkspaceMemberIdNotFound, InactiveWorkspaceMember, EmptyWorkspaceName, \
    InvalidWorkspaceIdsFound, \
    UnexpectedRole, WorkspaceMemberNotFound
from task_management.exceptions.enums import Role, Permissions
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface


class WorkspaceValidator:

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    def check_workspace_member_is_active_by_id(
            self, workspace_member_id: int):
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

        is_member_not_found = not workspace_member_data

        if is_member_not_found:
            raise WorkspaceMemberIdNotFound(
                workspace_member_id=workspace_member_id)

        if not workspace_member_data.is_active:
            raise InactiveWorkspaceMember(
                workspace_member_id=workspace_member_id)

    @staticmethod
    def check_workspace_name_not_empty(workspace_name: str):
        is_name_empty = not workspace_name or not workspace_name.strip()

        if is_name_empty:
            raise EmptyWorkspaceName(workspace_name=workspace_name)

    def check_workspace_ids(self, workspace_ids: list[str]):

        workspaces_data = self.workspace_storage.get_workspaces(
            workspace_ids=workspace_ids)

        existed_workspace_ids = [str(obj.workspace_id) for obj in
                                 workspaces_data]
        invalid_workspace_ids = [workspace_id for workspace_id in workspace_ids
                                 if
                                 str(workspace_id) not in existed_workspace_ids]

        if invalid_workspace_ids:
            raise InvalidWorkspaceIdsFound(
                workspace_ids=invalid_workspace_ids)

    @staticmethod
    def get_permission_type_by_role(role: str) -> Permissions:

        is_guest_role = role == Role.GUEST.value
        if is_guest_role:
            return Permissions.VIEW
        return Permissions.FULL_EDIT

    @staticmethod
    def check_role(role: str):

        existed_roles = Role.get_values()
        is_role_invalid = role not in existed_roles

        if is_role_invalid:
            raise UnexpectedRole(role=role)

    def check_workspace_member_is_active(
            self, workspace_id: str, user_id: str):

        workspace_member = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)

        is_member_not_found = not workspace_member
        if is_member_not_found:
            raise WorkspaceMemberNotFound(workspace_id=workspace_id,
                                          user_id=user_id)

        is_member_inactive = not workspace_member.is_active
        if is_member_inactive:
            raise InactiveWorkspaceMember(
                workspace_member_id=workspace_member.id)
