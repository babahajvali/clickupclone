from task_management.exceptions.custom_exceptions import \
    InactiveWorkspaceException, ModificationNotAllowedException
from task_management.interactors.storage_interfaces.workspace_storage_interface import \
    WorkspaceStorageInterface


class WorkspaceValidationMixin:
    def __init__(self, workspace_storage: WorkspaceStorageInterface, **kwargs):
        self.workspace_storage = workspace_storage
        super().__init__(**kwargs)

    def validate_workspace_exists(self, workspace_id: str):
        is_exists = self.workspace_storage.check_workspace_exists(
            workspace_id=workspace_id)

        if not is_exists:
            from task_management.exceptions.custom_exceptions import \
                WorkspaceNotFoundException
            raise WorkspaceNotFoundException(workspace_id=workspace_id)

    def validate_workspace_is_active(self, workspace_id: str):
        workspace_data = self.workspace_storage.get_workspace(workspace_id=workspace_id)

        if not workspace_data.is_active:
            raise InactiveWorkspaceException(workspace_id=workspace_id)




