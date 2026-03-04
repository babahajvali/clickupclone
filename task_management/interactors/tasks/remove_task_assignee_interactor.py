from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import TaskAssigneeNotFound, \
    InActiveTaskAssigneeFound
from task_management.interactors.dtos import TaskAssigneeDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, TaskStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class RemoveTaskAssigneeInteractor:

    def __init__(
            self, task_storage: TaskStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def remove_task_assignee(
            self, assign_id: str, user_id: str) -> TaskAssigneeDTO:

        assignee_data = self._check_task_assignee_exists(
            assign_id=assign_id)
        self._check_user_has_edit_access_for_task(
            task_id=assignee_data.task_id, user_id=user_id)

        return self.task_storage.remove_task_assignee(
            assign_id=assign_id)

    def _check_task_assignee_exists(self, assign_id: str) -> TaskAssigneeDTO:

        assignee_data = self.task_storage.get_task_assignee(
            assign_id=assign_id)

        is_assignee_not_found = not assignee_data
        if is_assignee_not_found:
            raise TaskAssigneeNotFound(assign_id=assign_id)

        if not assignee_data.is_active:
            raise InActiveTaskAssigneeFound(assign_id=assign_id)

        return assignee_data

    def _check_user_has_edit_access_for_task(self, task_id: str, user_id: str):
        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
