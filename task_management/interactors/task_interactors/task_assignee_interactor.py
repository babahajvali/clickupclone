from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    TaskAssigneeNotFoundException
from task_management.interactors.dtos import TaskAssigneeDTO, UserTasksDTO
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.task_assignee_storage_interface import \
    TaskAssigneeStorageInterface
from task_management.interactors.storage_interfaces.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class TaskAssigneeInteractor(ValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 task_assignee_storage: TaskAssigneeStorageInterface,
                 user_storage: UserStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface,):
        self.task_storage = task_storage
        self.task_assignee_storage = task_assignee_storage
        self.user_storage = user_storage
        self.workspace_member_storage = workspace_member_storage
        self.list_storage = list_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by: str) -> TaskAssigneeDTO:
        existing_assignment = self.task_assignee_storage.get_user_task_assignee(
            user_id=user_id, task_id=task_id,assigned_by=assigned_by
        )
        if existing_assignment:
            return self.task_assignee_storage.reassign_task_assignee(
                assign_id=existing_assignment.assign_id)
        self.validate_user_is_active(user_id=user_id,
                                     user_storage=self.user_storage)
        list_id = self.get_active_task_list_id(task_id=task_id,
                                               task_storage=self.task_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=assigned_by,
            workspace_member_storage=self.workspace_member_storage)

        return self.task_assignee_storage.assign_task_assignee(
            task_id=task_id, assigned_by=assigned_by, user_id=user_id)

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def remove_task_assignee(self, assign_id: str,
                             user_id: str) -> TaskAssigneeDTO:
        assignee_data = self._validate_task_assignee_exists(
            assign_id=assign_id)
        list_id = self.get_active_task_list_id(task_id=assignee_data.task_id,
                                               task_storage=self.task_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.task_assignee_storage.remove_task_assignee(
            assign_id=assign_id)

    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:
        self.get_active_task_list_id(task_id=task_id,
                                     task_storage=self.task_storage)

        return self.task_assignee_storage.get_task_assignees(task_id=task_id)

    @interactor_cache(timeout=30*60, cache_name="list_task_assignees")
    def get_list_task_assignees(self, list_id: str) -> list[TaskAssigneeDTO]:
        self.validate_list_is_active(list_id=list_id,list_storage=self.list_storage)

        return self.task_assignee_storage.get_list_task_assignees(list_id=list_id)

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        self.validate_user_is_active(user_id=user_id,
                                     user_storage=self.user_storage)

        return self.task_assignee_storage.get_user_assigned_tasks(
            user_id=user_id)

    def _validate_task_assignee_exists(self, assign_id: str):
        assignee_data = self.task_assignee_storage.get_task_assignee(
            assign_id=assign_id)

        if not assignee_data:
            raise TaskAssigneeNotFoundException(assign_id=assign_id)
        return assignee_data
