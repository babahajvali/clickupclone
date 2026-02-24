from task_management.decorators.caching_decorators import interactor_cache
from task_management.exceptions.custom_exceptions import \
    DeletedWorkspaceFound, ModificationNotAllowed, \
    UserNotWorkspaceOwner, WorkspaceNotFound, UserNotWorkspaceMember
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface


class WorkspaceValidationMixin:
    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    def check_workspace_is_active(self, workspace_id: str):
        workspace_data = self.workspace_storage.get_workspace(
            workspace_id=workspace_id)

        is_workspace_not_found = not workspace_data
        if is_workspace_not_found:
            raise WorkspaceNotFound(workspace_id=workspace_id)

        is_workspace_delete = workspace_data.is_deleted
        if is_workspace_delete:
            raise DeletedWorkspaceFound(workspace_id=workspace_id)

    def check_workspace_exists(self, workspace_id: str):
        is_workspace_exists = self.workspace_storage.is_workspace_exists(
            workspace_id=workspace_id)

        is_workspace_not_exists = not is_workspace_exists
        if is_workspace_not_exists:
            raise WorkspaceNotFound(workspace_id=workspace_id)

    def check_user_is_workspace_owner(self, user_id: str,
                                      workspace_id: str):
        is_owner = self.workspace_storage.validate_user_is_workspace_owner(
            workspace_id=workspace_id, user_id=user_id)

        if not is_owner:
            raise UserNotWorkspaceOwner(user_id=user_id)

    @interactor_cache(cache_name='validate_permission', timeout=5 * 60)
    def check_user_has_edit_access_to_workspace(
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
