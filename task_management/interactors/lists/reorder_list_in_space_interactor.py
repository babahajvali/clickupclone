from django.db import transaction

from task_management.decorators.caching_decorators import (
    invalidate_interactor_cache,
)
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import ListDTO
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.mixins import (
    ListValidationMixin,
    SpaceValidationMixin,
    WorkspaceValidationMixin,
)


class ReorderListInSpaceInteractor:

    def __init__(
            self, list_storage: ListStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface):
        self.list_storage = list_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="space_lists")
    def reorder_list_in_space(
            self, list_id: str, space_id: str, order: int, user_id: str) \
            -> ListDTO:
        self._check_list_order_within_range(space_id=space_id, order=order)
        self.list_mixin.check_list_not_deleted(list_id=list_id)
        self.space_mixin.check_space_not_deleted(space_id=space_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_id)

        list_data = self.list_storage.get_list(list_id=list_id)

        old_order = list_data.order
        if old_order == order:
            return list_data

        return self._reorder_lists_and_update_current_in_space(
            list_id=list_id,
            old_order=old_order,
            new_order=order,
            space_id=space_id,
        )

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )

    def _reorder_lists_and_update_current_in_space(
            self, space_id: str, old_order: int, new_order: int, list_id: str):

        self._shift_other_lists_in_space(
            space_id=space_id, old_order=old_order, new_order=new_order
        )

        return self.list_storage.update_list_order_in_space(
            list_id=list_id, order=new_order, space_id=space_id
        )

    def _shift_other_lists_in_space(
            self, space_id: str, old_order: int, new_order: int):

        if new_order > old_order:
            self.list_storage.shift_lists_down_in_space(
                space_id=space_id, old_order=old_order, new_order=new_order
            )
        else:
            self.list_storage.shift_lists_up_in_space(
                space_id=space_id, old_order=old_order, new_order=new_order
            )

    def _check_list_order_within_range(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        lists_count = self.list_storage.get_space_lists_count(
            space_id=space_id)

        if order > lists_count:
            raise InvalidOrder(order=order)
