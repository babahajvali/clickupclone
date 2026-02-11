from task_management.exceptions.custom_exceptions import \
    InactiveWorkspaceException, ModificationNotAllowedException, \
    UserNotWorkspaceOwnerException, WorkspaceNotFoundException
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
