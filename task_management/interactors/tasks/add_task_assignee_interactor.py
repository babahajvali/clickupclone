from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import TaskAssigneeDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, UserStorageInterface, WorkspaceStorageInterface
from task_management.mixins import TaskValidationMixin, UserValidationMixin, \
    WorkspaceValidationMixin


class AddTaskAssigneeInteractor(
        TaskValidationMixin,
        UserValidationMixin,
        WorkspaceValidationMixin):

    def __init__(
            self, task_storage: TaskStorageInterface,
            user_storage: UserStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            task_storage=task_storage,
            user_storage=user_storage,
            workspace_storage=workspace_storage,
        )
        self.task_storage = task_storage
        self.user_storage = user_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def add_task_assignee(
            self, task_id: str, user_id: str, assigned_by: str) \
            -> TaskAssigneeDTO:
        self.check_task_not_deleted(task_id=task_id)
        self.check_user_is_active(user_id=user_id)

        self._check_user_has_edit_access_for_task(
            task_id=task_id, user_id=assigned_by)

        assignee_data = self.task_storage.get_user_task_assignee(
            user_id=user_id, task_id=task_id, assigned_by=assigned_by)
        if assignee_data:
            if not assignee_data.is_active:
                return self.task_storage.reassign_task_assignee(
                    assign_id=assignee_data.assign_id)
            return assignee_data

        return self.task_storage.add_task_assignee(
            task_id=task_id, assigned_by=assigned_by, user_id=user_id)

    def _check_user_has_edit_access_for_task(self, task_id: str, user_id: str):
        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
