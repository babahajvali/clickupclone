from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import InvalidOrder
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TaskValidationMixin, \
    WorkspaceValidationMixin


class ReorderTaskInteractor:

    def __init__(
            self, task_storage: TaskStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def task_mixin(self) -> TaskValidationMixin:
        return TaskValidationMixin(task_storage=self.task_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="tasks")
    def reorder_task(self, task_id: str, order: int, user_id: str) -> TaskDTO:
        self.task_mixin.check_task_not_deleted(task_id=task_id)
        task_data = self.task_storage.get_task(task_id=task_id)
        self._check_task_order(
            list_id=task_data.list_id, order=order
        )
        self._check_user_has_edit_access_for_task(
            task_id=task_id, user_id=user_id)

        current_order = task_data.order

        if current_order == order:
            return task_data

        return self._reorder_task_positions(
            list_id=task_data.list_id, current_order=current_order,
            new_order=order, task_id=task_id)

    def _check_user_has_edit_access_for_task(self, task_id: str, user_id: str):
        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def _check_task_order(self, list_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        tasks_count = self.task_storage.get_tasks_count(
            list_id=list_id)

        if order > tasks_count:
            raise InvalidOrder(order=order)

    def _reorder_task_positions(
            self, list_id: str, current_order: int,
            new_order: int, task_id: str):

        self._reorder_task_positions_except_current(
            list_id=list_id, current_order=current_order, new_order=new_order)

        return self.task_storage.reorder_tasks(
            task_id=task_id, new_order=new_order, list_id=list_id)

    def _reorder_task_positions_except_current(
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
