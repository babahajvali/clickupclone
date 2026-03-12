from contextlib import AbstractContextManager

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    SpaceValidationMixin
from task_management.utils.redis_utils import redis_lock


class CreateSpaceInteractor(WorkspaceValidationMixin, SpaceValidationMixin):
    """
    Create Space Interactor creates a space inside a workspace.

    Handle the create space operation.
    This interactor checks the business rules and permission validation
     before creating the space.

    Key Responsibility:
     - Create the space

    Dependencies:
        - SpaceStorageInterface
        - WorkspaceStorageInterface
    """

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(workspace_storage=workspace_storage,
                         space_storage=space_storage)
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def create_space(self, create_space_dto: CreateSpaceDTO) -> SpaceDTO:
        """Create a new space for the target workspace."""
        self._check_create_space_input(create_space_dto=create_space_dto)
        self._check_user_has_edit_access_to_workspace_for_space(
            workspace_id=create_space_dto.workspace_id,
            user_id=create_space_dto.created_by,
        )

        with self._get_create_space_lock(
                workspace_id=create_space_dto.workspace_id):
            last_space_order_in_workspace = (
                self.space_storage.get_last_space_order_in_workspace(
                    workspace_id=create_space_dto.workspace_id
                )
            )

            space_dto = self.space_storage.create_space(
                create_space_dto=create_space_dto,
                order=last_space_order_in_workspace + 1,
            )
        return space_dto

    def _check_create_space_input(
            self, create_space_dto: CreateSpaceDTO) -> None:
        self.check_space_name_not_empty(name=create_space_dto.name)
        self.check_workspace_not_deleted(
            workspace_id=create_space_dto.workspace_id
        )

    def _check_user_has_edit_access_to_workspace_for_space(
            self, workspace_id: str, user_id: str) -> None:
        self.check_user_has_edit_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
        )

    @staticmethod
    def _get_create_space_lock(workspace_id: str) -> AbstractContextManager:
        lock_key = f"lock:create_space:workspace:{workspace_id}"
        return redis_lock(lock_key, timeout=10)
