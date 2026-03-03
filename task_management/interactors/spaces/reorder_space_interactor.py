from django.db import transaction

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class ReorderSpaceInteractor:

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="spaces")
    def reorder_space(
            self, workspace_id: str, space_id: str, order: int, user_id: str) \
            -> SpaceDTO:
        self._check_space_order(workspace_id=workspace_id, order=order)
        self.space_mixin.check_space_not_deleted(space_id=space_id)
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=workspace_id
        )
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )

        space_data = self.space_storage.get_space(space_id=space_id)
        current_order = space_data.order

        if current_order == order:
            return space_data

        return self._reorder_space_positions(
            space_id=space_id,
            current_order=current_order,
            new_order=order,
            workspace_id=workspace_id)

    def _check_space_order(self, workspace_id: str, order: int):

        if order < 1:
            raise InvalidOrder(order=order)
        space_count = self.space_storage.get_workspace_spaces_count(
            workspace_id=workspace_id)

        if order > space_count:
            raise InvalidOrder(order=order)

    def _reorder_space_positions(
            self, workspace_id: str, current_order: int,
            new_order: int, space_id: str) -> SpaceDTO:

        self._reorder_space_positions_except_current(
            workspace_id=workspace_id,
            current_order=current_order,
            new_order=new_order)

        return self.space_storage.update_space_order(
            space_id=space_id, new_order=new_order)

    def _reorder_space_positions_except_current(
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
