from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class DeleteSpaceInteractor(SpaceValidationMixin, WorkspaceValidationMixin):
    """
    Delete Space Interactor soft deletes a space.

    Handle the delete space operation.
    This interactor checks the business rules and permission validation
     before deleting the space.

    Key Responsibility:
     - Delete the space

    Dependencies:
        - SpaceStorageInterface
        - WorkspaceStorageInterface
    """

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(space_storage=space_storage,
                         workspace_storage=workspace_storage)
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def delete_space(self, space_id: str, deleted_by: str) -> SpaceDTO:
        """Soft delete a space after existence and permission checks."""
        self.check_space_exists(space_id=space_id)
        self._check_user_has_edit_access_to_space(
            space_id=space_id,
            user_id=deleted_by,
        )

        return self.space_storage.delete_space(space_id=space_id)

    def _check_user_has_edit_access_to_space(
            self, space_id: str, user_id: str) -> None:
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id
        )

        self.check_user_has_edit_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
        )
