from django.db import transaction
from contextlib import AbstractContextManager

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache, redis_lock
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class ReorderSpaceInteractor(SpaceValidationMixin, WorkspaceValidationMixin):
    """
    Reorder Space Interactor reorders spaces inside a workspace.

    Handle the reorder space operation.
    This interactor checks the business rules and permission validation
     before reordering the space.

    Key Responsibility:
     - Reorder the space

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

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="spaces")
    def reorder_space(
            self, workspace_id: str, space_id: str, order: int, user_id: str) \
            -> SpaceDTO:
        """Move a space to a new position after validations and access checks."""

        self.check_workspace_not_deleted(workspace_id=workspace_id)
        self.check_space_not_deleted(space_id=space_id)
        self._check_user_has_edit_access_to_workspace_for_space(
            workspace_id=workspace_id,
            user_id=user_id,
        )

        with self._get_reorder_space_lock(workspace_id=workspace_id):
            self._check_space_order_within_range(
                workspace_id=workspace_id,
                order=order,
            )
            space_dto = self.space_storage.get_space(space_id=space_id)
            current_order = space_dto.order

            if current_order == order:
                return space_dto

            updated_space_dto = self._reorder_spaces_and_update_current(
                space_id=space_id,
                current_order=current_order,
                new_order=order,
                workspace_id=workspace_id,
            )
        return updated_space_dto

    def _check_space_order_within_range(self, workspace_id: str, order: int):

        if order < 1:
            raise InvalidOrder(order=order)
        space_count = self.space_storage.get_workspace_spaces_count(
            workspace_id=workspace_id)

        if order > space_count:
            raise InvalidOrder(order=order)

    def _reorder_spaces_and_update_current(
            self, workspace_id: str, current_order: int,
            new_order: int, space_id: str) -> SpaceDTO:

        self._shift_other_spaces(
            workspace_id=workspace_id,
            current_order=current_order,
            new_order=new_order)

        return self.space_storage.update_space_order(
            space_id=space_id, new_order=new_order)

    def _shift_other_spaces(
            self, workspace_id: str, current_order: int, new_order: int):

        if new_order > current_order:
            self.space_storage.shift_spaces_down(
                workspace_id=workspace_id, current_order=current_order,
                new_order=new_order
            )
        else:
            self.space_storage.shift_spaces_up(
                workspace_id=workspace_id, current_order=current_order,
                new_order=new_order
            )

    def _check_user_has_edit_access_to_workspace_for_space(
            self, workspace_id: str, user_id: str) -> None:
        self.check_user_has_edit_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
        )

    @staticmethod
    def _get_reorder_space_lock(workspace_id: str) -> AbstractContextManager:
        lock_key = f"lock:reorder_space:workspace:{workspace_id}"
        return redis_lock(lock_key, timeout=10)
