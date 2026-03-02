from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator


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

    @property
    def workspace_validator(self) -> WorkspaceValidator:
        return WorkspaceValidator(workspace_storage=self.workspace_storage)

    def get_workspaces(
            self, workspace_ids: list[str]) -> list[WorkspaceDTO]:
        self.workspace_validator.check_workspace_ids(
            workspace_ids=workspace_ids
        )

        return self.workspace_storage.get_workspaces(
            workspace_ids=workspace_ids
        )
