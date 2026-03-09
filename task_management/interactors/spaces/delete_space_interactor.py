from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class DeleteSpaceInteractor(SpaceValidationMixin, WorkspaceValidationMixin):

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(space_storage=space_storage,
                         workspace_storage=workspace_storage)
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def delete_space(self, space_id: str, deleted_by: str) -> SpaceDTO:
        self.check_space_exists(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id
        )
        self.check_user_has_edit_access_to_workspace(
            user_id=deleted_by, workspace_id=workspace_id
        )

        return self.space_storage.delete_space(space_id=space_id)
