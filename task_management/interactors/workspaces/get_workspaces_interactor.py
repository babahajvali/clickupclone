from task_management.exceptions.custom_exceptions import \
    InvalidWorkspaceIdsFound
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface


class WorkspaceInteractor:
    """Retrieve Workspace Management Business Logic Interactor.
    
    Handles retrieval of workspaces. This interactor validates workspace-ids before
     performing any workspaces operations.
    
    Key Responsibilities:
        - Retrieve workspaces information

    Dependencies:
        - WorkspaceStorageInterface: Workspace data persistence
    
    Attributes:
        workspace_storage (WorkspaceStorageInterface): Storage for workspaces operations
    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    def get_workspaces(
            self, workspace_ids: list[str]) -> list[WorkspaceDTO]:
        self._check_workspace_ids(
            workspace_ids=workspace_ids
        )

        return self.workspace_storage.get_workspaces(
            workspace_ids=workspace_ids
        )

    def _check_workspace_ids(self, workspace_ids: list[str]):
        workspaces_data = self.workspace_storage.get_workspaces(
            workspace_ids=workspace_ids)

        existed_workspace_ids = [str(obj.workspace_id) for obj in
                                 workspaces_data]
        invalid_workspace_ids = [
            workspace_id for workspace_id in workspace_ids if
            str(workspace_id) not in existed_workspace_ids]

        if invalid_workspace_ids:
            raise InvalidWorkspaceIdsFound(
                workspace_ids=invalid_workspace_ids)
