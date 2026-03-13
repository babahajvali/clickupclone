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
from task_management.utils.redis_utils import redis_lock


class ReorderListInSpaceInteractor(
    ListValidationMixin,
    SpaceValidationMixin,
    WorkspaceValidationMixin):

    def __init__(
            self, list_storage: ListStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface):
        super().__init__(
            list_storage=list_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage,
        )
        self.list_storage = list_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="space_lists")
    def reorder_list_in_space(
            self, list_id: str, space_id: str, order: int, user_id: str) \
            -> ListDTO:

        self.check_list_not_deleted(list_id=list_id)
        self.check_space_not_deleted(space_id=space_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_id)

        lock_key = f"lock:reorder_list:space:{space_id}"
        with redis_lock(lock_key, timeout=10):
            self._check_list_order_within_range(space_id=space_id, order=order)
            list_data = self.list_storage.get_list(list_id=list_id)

            old_order = list_data.order
            if old_order == order:
                return list_data

            updated_list_dto = self._reorder_lists_and_update_current_in_space(
                list_id=list_id,
                old_order=old_order,
                new_order=order,
                space_id=space_id,
            )
        return updated_list_dto

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.check_user_has_edit_access_to_workspace(
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
