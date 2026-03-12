from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class DeleteWorkspaceInteractor(WorkspaceValidationMixin):

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        super().__init__(workspace_storage=workspace_storage)
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(
            self, workspace_id: str, user_id: str) -> WorkspaceDTO:
        self.check_workspace_exists(
            workspace_id=workspace_id
        )
        self.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id
        )

        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id
        )
