from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class GetWorkspaceSpacesInteractor:

    def __init__(self, space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @interactor_cache(cache_name="spaces", timeout=30 * 60)
    def get_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=workspace_id
        )

        return self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)
