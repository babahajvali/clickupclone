from django.db import transaction

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TaskValidationMixin, \
    WorkspaceValidationMixin
from task_management.utils.redis_utils import redis_lock


class ReorderTaskInteractor(TaskValidationMixin, WorkspaceValidationMixin):

    def __init__(
            self, task_storage: TaskStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            task_storage=task_storage,
            workspace_storage=workspace_storage,
        )
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    @invalidate_interactor_cache(cache_name="tasks")
    def reorder_task(self, task_id: str, order: int, user_id: str) -> TaskDTO:
        self.check_task_not_deleted(task_id=task_id)
        self._check_user_has_edit_access_for_task(
            task_id=task_id, user_id=user_id)

        lock_key = f"lock:reorder_task:task:{task_id}"
        with redis_lock(lock_key, timeout=10):
            task_dto = self.task_storage.get_task(task_id=task_id)
            self._check_task_order_within_range(
                list_id=task_dto.list_id,
                order=order,
            )

            current_order = task_dto.order

            if current_order == order:
                return task_dto

            updated_task_dto = self._reorder_tasks_and_update_current(
                list_id=task_dto.list_id,
                current_order=current_order,
                new_order=order,
                task_id=task_id,
            )
        return updated_task_dto

    def _check_user_has_edit_access_for_task(self, task_id: str, user_id: str):
        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def _check_task_order_within_range(self, list_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        tasks_count = self.task_storage.get_tasks_count(
            list_id=list_id)

        if order > tasks_count:
            raise InvalidOrder(order=order)

    def _reorder_tasks_and_update_current(
            self, list_id: str, current_order: int,
            new_order: int, task_id: str):

        self._shift_other_tasks(
            list_id=list_id, current_order=current_order, new_order=new_order)

        return self.task_storage.reorder_task(
            task_id=task_id, new_order=new_order, list_id=list_id)

    def _shift_other_tasks(
            self, list_id: str, current_order: int, new_order: int):

        if new_order > current_order:
            self.task_storage.shift_tasks_down(
                list_id=list_id, current_order=current_order,
                new_order=new_order)
        else:
            self.task_storage.shift_tasks_up(
                list_id=list_id, current_order=current_order,
                new_order=new_order
            )
