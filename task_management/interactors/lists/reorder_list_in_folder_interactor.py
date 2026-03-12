from django.db import transaction

from task_management.decorators.caching_decorators import (
    invalidate_interactor_cache,
)
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import ListDTO

from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.mixins import (
    ListValidationMixin,
    WorkspaceValidationMixin,
    FolderValidationMixin,
)
from task_management.utils.redis_utils import redis_lock


class ReorderListInFolderInteractor(
        ListValidationMixin,
        WorkspaceValidationMixin,
        FolderValidationMixin):

    def __init__(
            self, list_storage: ListStorageInterface,
            folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            list_storage=list_storage,
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
        )
        self.list_storage = list_storage
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="folder_lists")
    def reorder_list_in_folder(
            self, folder_id: str, list_id: str, order: int, user_id: str) \
            -> ListDTO:
        self.check_list_not_deleted(list_id=list_id)
        self.check_folder_not_deleted(folder_id=folder_id)
        self._check_user_has_edit_access_for_list(
            list_id=list_id, user_id=user_id)

        lock_key = f"lock:reorder_list:folder:{folder_id}"
        with redis_lock(lock_key, timeout=10):
            self._check_list_order_within_range(folder_id=folder_id, order=order)
            list_data = self.list_storage.get_list(list_id=list_id)

            old_order = list_data.order

            if old_order == order:
                return list_data

            updated_list_dto = self._reorder_lists_and_update_current_in_folder(
                list_id=list_id,
                old_order=old_order,
                new_order=order,
                folder_id=folder_id,
            )
        return updated_list_dto

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):

        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )

    def _check_list_order_within_range(self, folder_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)

        lists_count = self.list_storage.get_folder_lists_count(
            folder_id=folder_id)

        if order > lists_count:
            raise InvalidOrder(order=order)

    def _reorder_lists_and_update_current_in_folder(
            self, folder_id: str, list_id: str, old_order: int, new_order: int
    ):

        self._shift_other_lists_in_folder(
            folder_id=folder_id, old_order=old_order, new_order=new_order
        )

        return self.list_storage.update_list_order_in_folder(
            list_id=list_id, order=new_order, folder_id=folder_id
        )

    def _shift_other_lists_in_folder(
            self, folder_id: str, old_order: int, new_order: int):

        if new_order > old_order:
            self.list_storage.shift_lists_down_in_folder(
                folder_id=folder_id, old_order=old_order, new_order=new_order
            )
        else:
            self.list_storage.shift_lists_up_in_folder(
                folder_id=folder_id, old_order=old_order, new_order=new_order
            )
