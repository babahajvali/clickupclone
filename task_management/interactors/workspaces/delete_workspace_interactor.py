from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class DeleteWorkspaceInteractor:

    def __init__(self, workspace_storage: WorkspaceStorageInterface):
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(
            self, workspace_id: str, user_id: str) -> WorkspaceDTO:
        self.workspace_mixin.validate_workspace_exists(
            workspace_id=workspace_id
        )
        self.workspace_mixin.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id
        )

        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id
        )
