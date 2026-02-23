from typing import Optional
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, FilterDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.interactors.tasks.validators.task_validator import \
    TaskValidator
from task_management.mixins import WorkspaceValidationMixin, \
    ListValidationMixin, TaskValidationMixin


class TaskInteractor:
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def task_mixin(self) -> TaskValidationMixin:
        return TaskValidationMixin(task_storage=self.task_storage)

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def task_validator(self) -> TaskValidator:
        return TaskValidator(task_storage=self.task_storage)

    @invalidate_interactor_cache(cache_name="tasks")
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        self.task_validator.check_task_title_not_empty(title=task_data.title)
        self.list_mixin.check_list_is_active(list_id=task_data.list_id)
        self._check_user_has_edit_access_for_list(
            list_id=task_data.list_id, user_id=task_data.created_by)

        order = self.task_storage.get_next_task_order_in_list(
            list_id=task_data.list_id)

        return self.task_storage.create_task(task_data=task_data, order=order)

    @invalidate_interactor_cache(cache_name="tasks")
    def update_task(
            self, task_id: str, user_id: str, title: Optional[str],
            description: Optional[str]) -> TaskDTO:
        self.task_mixin.check_task_is_active(task_id=task_id)
        field_properties_to_update = (
            self.task_validator.check_task_update_field_properties(
                task_id=task_id, title=title, description=description))

        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self.list_mixin.check_list_is_active(list_id=list_id)
        self._check_user_has_edit_access_for_list(
            list_id=list_id, user_id=user_id)

        return self.task_storage.update_task(
            task_id=task_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="tasks")
    def delete_task(self, task_id: str, user_id: str) -> TaskDTO:
        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self._check_user_has_edit_access_for_list(list_id=list_id,
                                                  user_id=user_id)

        return self.task_storage.remove_task(task_id=task_id)

    @interactor_cache(cache_name="tasks", timeout=5 * 60)
    def get_active_tasks_for_list(self, list_id: str) -> list[TaskDTO]:
        self.list_mixin.check_list_is_active(list_id=list_id)

        return self.task_storage.get_active_tasks_for_list(list_id=list_id)

    def get_task(self, task_id: str) -> TaskDTO:
        self.task_mixin.check_task_is_active(task_id=task_id)

        return self.task_storage.get_task_by_id(task_id=task_id)

    def task_filter(self, task_filter_data: FilterDTO):
        self.task_validator.check_filter_parameters(
            filter_data=task_filter_data)
        self.list_mixin.check_list_is_active(list_id=task_filter_data.list_id)


        return self.task_storage.task_filter_data(filter_data=task_filter_data)

    @invalidate_interactor_cache(cache_name="tasks")
    def reorder_task(self, task_id: str, order: int, user_id: str) -> TaskDTO:

        self.task_mixin.check_task_is_active(task_id=task_id)
        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self.task_validator.check_task_order(list_id=list_id, order=order)
        self._check_user_has_edit_access_for_list(
            list_id=list_id, user_id=user_id)

        return self.task_storage.reorder_tasks(
            task_id=task_id, new_order=order, list_id=list_id)

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):

        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.workspace_mixin.check_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
