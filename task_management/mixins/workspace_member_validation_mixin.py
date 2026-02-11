from task_management.exceptions.custom_exceptions import \
    WorkspaceNotFoundException, ModificationNotAllowedException
from task_management.interactors.storage_interfaces import \
    WorkspaceMemberStorageInterface


class WorkspaceMemberValidationMixin:
    def __init__(self, workspace_member_storage: WorkspaceMemberStorageInterface):
        self.workspace_member_storage = workspace_member_storage

    def validate_user_access_for_workspace(self, user_id: str, workspace_id: str):
        workspace_data = self.workspace_member_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)

        if workspace_data is None:
            raise WorkspaceNotFoundException(workspace_id=workspace_id)

        if str(workspace_data.user_id) != str(user_id):
            raise ModificationNotAllowedException(user_id=user_id)

