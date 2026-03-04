from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TaskValidationMixin, \
    WorkspaceValidationMixin


class DeleteTaskInteractor:

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
    def delete_task(self, task_id: str, user_id: str) -> TaskDTO:
        self.task_mixin.check_task_exists(task_id=task_id)
        self._check_user_has_edit_access_for_task(
            task_id=task_id, user_id=user_id)

        return self.task_storage.delete_task(task_id=task_id)

    def _check_user_has_edit_access_for_task(self, task_id: str, user_id: str):
        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
