from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.mixins import ListValidationMixin, \
    WorkspaceValidationMixin, TaskValidationMixin


class CreateTaskInteractor:

    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def task_mixin(self) -> TaskValidationMixin:
        return TaskValidationMixin(task_storage=self.task_storage)

    @invalidate_interactor_cache(cache_name="tasks")
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        self.task_mixin.check_task_title_not_empty(title=task_data.title)
        self.list_mixin.check_list_not_deleted(list_id=task_data.list_id)
        self._check_user_has_edit_access_for_list(
            list_id=task_data.list_id, user_id=task_data.created_by)

        order = self.task_storage.get_last_task_order_in_list(
            list_id=task_data.list_id)

        return self.task_storage.create_task(
            task_data=task_data, order=order + 1)

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
